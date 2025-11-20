"""
Toy Trip Generator with AI-generated gallery images.

Generates trip itineraries for toys from toy_profiles.json with famous destinations and
AI-generated gallery images featuring the toy at various landmarks using
Azure OpenAI GPT and image generation models.
"""
import base64
import json
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, TypeVar
from uuid import uuid4

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI, RateLimitError, APIError
from PIL import Image
from pydantic import BaseModel, Field


T = TypeVar('T')


T = TypeVar('T')


def retry_with_exponential_backoff(
    func: Callable[..., T],
    max_retries: int = 5,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> Callable[..., T]:
    """
    Decorator to retry a function with exponential backoff on rate limit errors.

    Args:
        func: Function to wrap with retry logic.
        max_retries: Maximum number of retry attempts.
        initial_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay in seconds between retries.
        backoff_factor: Multiplier for delay after each retry.

    Returns:
        Wrapped function with retry logic.
    """
    def wrapper(*args, **kwargs) -> T:
        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                last_exception = e
                if attempt == max_retries:
                    raise
                
                print(f"         ⏳ Rate limit hit, retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
                delay = min(delay * backoff_factor, max_delay)
            except APIError as e:
                # Retry on 5xx server errors, but not on 4xx client errors (except 429)
                if hasattr(e, 'status_code') and 500 <= e.status_code < 600:
                    last_exception = e
                    if attempt == max_retries:
                        raise
                    
                    print(f"         ⏳ Server error ({e.status_code}), retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
                else:
                    # Don't retry on other errors
                    raise

        raise last_exception

    return wrapper


class FamousDestination(BaseModel):
    """Famous travel destination with landmarks."""

    location_name: str = Field(..., description="City or location name")
    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    famous_landmarks: list[str] = Field(
        ..., description="List of 5-10 famous landmarks at this location"
    )
    description: str = Field(..., description="Brief description of why it's special")


class DestinationsList(BaseModel):
    """List of famous destinations."""

    destinations: list[FamousDestination] = Field(
        ..., description="List of 30+ famous travel destinations"
    )


class TripToDestination(BaseModel):
    """Trip to a single destination."""

    trip_title: str = Field(..., description="Creative trip title (e.g., 'Globetot's Parisian Adventure')")
    trip_description: str = Field(..., description="Fun trip description (2-3 sentences)")
    location_name: str = Field(..., description="Destination city or location name")
    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code")


class GalleryImagePrompt(BaseModel):
    """Gallery image generation prompt."""

    landmark: str = Field(..., description="Specific landmark name")
    scene_description: str = Field(
        ..., description="Detailed prompt for image generation"
    )


def load_config() -> dict[str, Any]:
    """
    Load configuration from .env file.

    Returns:
        Dictionary with configuration values.

    Raises:
        ValueError: If required environment variables are missing.
    """
    load_dotenv()

    config = {
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "gpt_model": os.getenv("GPT_DEPLOYMENT_NAME"),
        "image_model": os.getenv("IMAGE_DEPLOYMENT_NAME"),
        "min_trips_per_toy": int(os.getenv("MIN_TRIPS_PER_TOY", "1")),
        "max_trips_per_toy": int(os.getenv("MAX_TRIPS_PER_TOY", "3")),
        "min_images_per_trip": int(os.getenv("MIN_IMAGES_PER_TRIP", "3")),
        "max_images_per_trip": int(os.getenv("MAX_IMAGES_PER_TRIP", "8")),
    }

    missing = [k for k, v in config.items() if not v and k not in [
        "min_trips_per_toy",
        "max_trips_per_toy",
        "min_images_per_trip",
        "max_images_per_trip",
    ]]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return config


def create_openai_client(endpoint: str) -> AzureOpenAI:
    """
    Create authenticated AzureOpenAI client using DefaultAzureCredential.
    
    Excludes SharedTokenCacheCredential to avoid authority validation issues
    in development environments (see docs/COMMON_ERRORS.md).

    Args:
        endpoint: Azure OpenAI endpoint URL.

    Returns:
        Configured AzureOpenAI client instance.
    """
    # Exclude shared token cache to avoid credential issues
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(exclude_shared_token_cache_credential=True),
        "https://cognitiveservices.azure.com/.default",
    )

    return AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2025-01-01-preview",
    )


def load_toy_profiles(profiles_path: Path, images_dir: Path) -> list[dict[str, Any]]:
    """
    Load toy profiles from toy_profiles.json.

    Args:
        profiles_path: Path to toy_profiles.json.
        images_dir: Directory containing avatar images.

    Returns:
        List of toy dictionaries with validated avatar paths.

    Raises:
        SystemExit: If profiles file not found.
    """
    if not profiles_path.exists():
        print(f"❌ Toy profiles not found at: {profiles_path}")
        print("   Run: python tools/data/toy-profile-generator/main.py")
        sys.exit(1)

    try:
        with open(profiles_path, "r", encoding="utf-8") as f:
            toys = json.load(f)

        # Validate avatars exist
        validated_toys = []
        for toy in toys:
            avatar_path = images_dir / toy["avatar_blob_name"]
            if avatar_path.exists():
                validated_toys.append(toy)
            else:
                print(f"   ⚠️  Missing avatar for {toy['name']}, skipping...")

        return validated_toys

    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error loading toy profiles: {e}")
        sys.exit(1)


def load_toy_avatar(images_dir: Path, blob_name: str) -> bytes | None:
    """
    Load toy avatar image from local file.

    Args:
        images_dir: Directory containing avatar images.
        blob_name: Avatar image filename.

    Returns:
        Image bytes or None if file doesn't exist.
    """
    avatar_path = images_dir / blob_name
    if not avatar_path.exists():
        return None

    try:
        with open(avatar_path, "rb") as f:
            return f.read()
    except IOError:
        return None


def load_or_generate_destinations(
    client: AzureOpenAI, model: str, cache_path: Path
) -> list[FamousDestination]:
    """
    Load destinations from cache or generate if not exists.

    Args:
        client: OpenAI client instance.
        model: GPT model deployment name.
        cache_path: Path to destinations cache file.

    Returns:
        List of FamousDestination objects.
    """
    # Try to load from cache
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                destinations = [FamousDestination(**d) for d in data]
                print(f"✅ Loaded {len(destinations)} destinations from cache")
                return destinations
        except (json.JSONDecodeError, Exception) as e:
            print(f"⚠️  Cache load failed ({e}), regenerating...")

    # Generate new destinations
    @retry_with_exponential_backoff
    def _generate():
        prompt = """Generate a diverse list of 50+ famous travel destinations around the world.

For each destination, include:
- Location name (city or specific place)
- ISO 3166-1 alpha-2 country code
- 5-10 famous landmarks at that location (be specific - Eiffel Tower, not just "tower")
- Brief description of what makes it special

Include variety:
- Different continents
- Mix of modern cities and ancient sites
- Natural wonders and man-made landmarks
- Popular tourist destinations and hidden gems

Examples:
- Paris, France (FR): Eiffel Tower, Louvre, Arc de Triomphe, Notre-Dame, Sacré-Cœur
- Rome, Italy (IT): Colosseum, Trevi Fountain, Pantheon, Vatican, Spanish Steps
- Machu Picchu, Peru (PE): Inca citadel, Temple of the Sun, Intihuatana stone
"""

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel expert with deep knowledge of world-famous destinations and landmarks.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=DestinationsList,
            reasoning_effort="minimal",
        )

        return completion.choices[0].message.parsed.destinations

    destinations = _generate()

    # Save to cache
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump([d.model_dump() for d in destinations], f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated and cached {len(destinations)} destinations")
    return destinations


def generate_trip_to_destination(
    client: AzureOpenAI,
    model: str,
    toy_name: str,
    destination: FamousDestination,
) -> TripToDestination:
    """
    Generate trip for a toy to a single destination.

    Args:
        client: OpenAI client instance.
        model: GPT model deployment name.
        toy_name: Name of the toy.
        destination: Destination to visit.

    Returns:
        TripToDestination object.
    """
    @retry_with_exponential_backoff
    def _generate():
        prompt = f"""Create a fun trip for {toy_name}, a toy visiting {destination.location_name}, {destination.country_code}!

Destination info:
{destination.description}

Famous landmarks: {', '.join(destination.famous_landmarks[:5])}

Requirements:
- Creative trip title (e.g., "{toy_name}'s Parisian Adventure")
- Fun 2-3 sentence description about what {toy_name} will do and see in {destination.location_name}
- Make it playful and exciting for a toy's perspective
"""

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel planner creating exciting single-destination adventures for toys.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=TripToDestination,
            reasoning_effort="minimal",
        )

        return completion.choices[0].message.parsed

    return _generate()


def generate_gallery_prompts(
    client: AzureOpenAI,
    model: str,
    toy_name: str,
    location: str,
    landmarks: list[str],
    num_images: int,
) -> list[GalleryImagePrompt]:
    """
    Generate image prompts for gallery.

    Args:
        client: OpenAI client instance.
        model: GPT model deployment name.
        toy_name: Name of the toy.
        location: Location name.
        landmarks: Available landmarks.
        num_images: Number of images to generate prompts for.

    Returns:
        List of GalleryImagePrompt objects.
    """
    @retry_with_exponential_backoff
    def _generate():
        landmarks_str = ", ".join(landmarks[:10])  # Limit to avoid token overflow

        prompt = f"""Generate {num_images} diverse photo scene descriptions for {toy_name} visiting {location}.

Available landmarks: {landmarks_str}

For each scene:
- Choose a specific landmark
- Describe a detailed, photorealistic scene
- Vary distance (close-up, medium, wide), angle (low, eye-level, aerial), time of day
- Make each scene visually distinct and interesting

Remember: These will be used with image editing to place the toy into the scene, so describe the landmark/location clearly.
"""

        class GalleryPrompts(BaseModel):
            prompts: list[GalleryImagePrompt]

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional travel photographer planning diverse, visually striking shots.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=GalleryPrompts,
            reasoning_effort="minimal",
        )

        return completion.choices[0].message.parsed.prompts

    return _generate()


def generate_gallery_image(
    client: AzureOpenAI,
    model: str,
    toy_name: str,
    toy_description: str,
    prompt: str,
    output_path: Path,
) -> None:
    """
    Generate gallery image using DALL-E text-to-image generation.

    Args:
        client: AzureOpenAI client instance.
        model: Image generation model deployment name.
        toy_name: Name of the toy.
        toy_description: Description of the toy's appearance.
        prompt: Scene description for image generation.
        output_path: Path to save the generated image.
    """
    @retry_with_exponential_backoff
    def _generate():
        # Generate image from text prompt describing toy + scene
        full_prompt = f"A photograph of {toy_name}, {toy_description}, at {prompt}. Photorealistic travel photography style, high quality."
        
        response = client.images.generate(
            model=model,
            prompt=full_prompt,
            n=1,
            size="1024x1024",
        )

        # gpt-image-1 returns base64-encoded images
        image_base64 = response.data[0].b64_json
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

        # Resize to 512x512 for gallery
        resized = image.resize((512, 512), Image.Resampling.LANCZOS)
        resized.save(output_path, "JPEG", quality=85, optimize=True)

    _generate()


def generate_single_image_task(
    client: AzureOpenAI,
    model: str,
    toy_name: str,
    toy_description: str,
    prompt_obj: GalleryImagePrompt,
    leg_idx: int,
    images_dir: Path,
) -> dict[str, Any] | None:
    """
    Generate a single gallery image (designed for parallel execution).

    Args:
        client: AzureOpenAI client instance.
        model: Image generation model deployment name.
        toy_name: Name of the toy.
        toy_description: Description of the toy's appearance.
        prompt_obj: Gallery image prompt object.
        leg_idx: Not used anymore (kept for compatibility).
        images_dir: Directory to save images.

    Returns:
        Gallery image metadata dict, or None if generation failed.
    """
    image_id = str(uuid4())
    blob_name = f"{image_id}.jpg"
    image_path = images_dir / blob_name

    try:
        generate_gallery_image(
            client,
            model,
            toy_name,
            toy_description,
            prompt_obj.scene_description,
            image_path,
        )

        return {
            "image_id": image_id,
            "blob_name": blob_name,
            "landmark": prompt_obj.landmark,
            "caption": f"{toy_name} at {prompt_obj.landmark}",
            "source": "generated",
        }

    except Exception as e:
        print(f"         ❌ Error generating {prompt_obj.landmark}: {e}")
        return None



def load_existing_data(
    output_file: Path, images_dir: Path
) -> tuple[list[dict[str, Any]], set[str]]:
    """
    Load existing trip data and validate images.

    Args:
        output_file: Path to JSON output file.
        images_dir: Directory containing trip images.

    Returns:
        Tuple of (trip list, set of existing toy IDs).
    """
    if not output_file.exists():
        return [], set()

    try:
        with open(output_file, encoding="utf-8") as f:
            trips = json.load(f)

        # Validate structure
        if not isinstance(trips, list):
            print(f"⚠️  Invalid format in {output_file}, starting fresh")
            return [], set()

        # Extract toy IDs that already have trips
        toy_ids = {trip["toy_id"] for trip in trips if "toy_id" in trip}

        # Validate images exist
        validated_trips = []
        for trip in trips:
            trip_valid = True
            for image in trip.get("gallery_images", []):
                image_path = images_dir / image["blob_name"]
                if not image_path.exists():
                    print(
                        f"⚠️  Missing image: {image['blob_name']} for trip {trip.get('trip_id')}"
                    )
                    trip_valid = False
                    break

            if trip_valid:
                validated_trips.append(trip)

        return validated_trips, toy_ids

    except (json.JSONDecodeError, KeyError) as e:
        print(f"⚠️  Error loading {output_file}: {e}")
        return [], set()


def save_trips(output_file: Path, trips: list[dict[str, Any]]) -> None:
    """
    Save trips to JSON file.

    Args:
        output_file: Path to JSON output file.
        trips: List of trip dictionaries to save.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(trips, f, indent=2, ensure_ascii=False)


def main():
    """Generate toy trips with AI-generated gallery images."""
    print("🗺️  Toy Trip Generator")
    print("=" * 70)

    try:
        # Load configuration
        config = load_config()
        print(f"✅ Configuration loaded")
        print(f"   OpenAI Endpoint: {config['endpoint']}")
        print(f"   GPT Model: {config['gpt_model']}")
        print(f"   Image Model: {config['image_model']}")
        print(
            f"   Trips per toy: {config['min_trips_per_toy']}-{config['max_trips_per_toy']}"
        )
        print(
            f"   Images per trip: {config['min_images_per_trip']}-{config['max_images_per_trip']}"
        )

        # Setup paths
        output_file = Path(__file__).parent.parent / "trips.json"
        images_dir = Path(__file__).parent.parent / "trip-images"
        images_dir.mkdir(exist_ok=True)
        
        destinations_cache = Path(__file__).parent / "destinations.json"
        toy_profiles_path = Path(__file__).parent.parent / "toy_profiles.json"
        toy_images_dir = Path(__file__).parent.parent / "toy-images"

        print(f"   Output file: {output_file}")
        print(f"   Images directory: {images_dir}")
        print(f"   Destinations cache: {destinations_cache}")
        print(f"   Toy profiles: {toy_profiles_path}")
        print()

        # Load toy profiles
        print("🧸 Loading toy profiles...")
        toys = load_toy_profiles(toy_profiles_path, toy_images_dir)
        print(f"✅ Loaded {len(toys)} toys")
        print()

        if not toys:
            print("❌ No toys found. Run toy-profile-generator first.")
            sys.exit(1)

        # Load existing data
        print("📂 Checking for existing trips...")
        existing_trips, existing_toy_ids = load_existing_data(output_file, images_dir)
        print(f"   Found {len(existing_trips)} existing trips")
        print(f"   {len(existing_toy_ids)} toys already have trips")
        print()

        # Filter toys that need trips
        toys_needing_trips = [t for t in toys if t["id"] not in existing_toy_ids]

        if not toys_needing_trips:
            print("✨ All toys already have trips!")
            return 0

        print(f"🎯 Generating trips for {len(toys_needing_trips)} toys")
        print()

        # Create OpenAI client
        print("🤖 Initializing OpenAI client...")
        client = create_openai_client(config["endpoint"])
        print("✅ OpenAI client ready")
        print()

        # Load or generate famous destinations
        print("🌍 Loading destinations...")
        destinations = load_or_generate_destinations(client, config["gpt_model"], destinations_cache)
        print()

        # Generate trips
        all_trips = existing_trips.copy()
        total_toys = len(toys_needing_trips)

        for toy_idx, toy in enumerate(toys_needing_trips, 1):
            toy_id = toy["id"]
            toy_name = toy["name"]
            avatar_blob_name = toy.get("avatar_blob_name")

            print(f"\n{'='*70}")
            print(f"[{toy_idx}/{total_toys}] Processing: {toy_name}")
            print(f"{'='*70}")

            # Get toy description for image generation
            toy_description = toy.get("description", f"a small toy named {toy_name}")
            print(f"   📝 Toy description: {toy_description[:100]}...")

            # Determine number of trips for this toy
            num_trips = random.randint(
                config["min_trips_per_toy"], config["max_trips_per_toy"]
            )
            print(f"   🎲 Generating {num_trips} trip(s)")

            for trip_num in range(1, num_trips + 1):
                print(f"\n   --- Trip {trip_num}/{num_trips} ---")

                # Select a random destination for this trip
                destination = random.choice(destinations)
                
                # Generate trip to destination
                print(f"   📋 Generating trip to {destination.location_name}...")
                trip = generate_trip_to_destination(
                    client, config["gpt_model"], toy_name, destination
                )
                print(f"   ✅ Trip: {trip.trip_title}")
                print(f"      Destination: {trip.location_name}, {trip.country_code}")

                # Build trip data
                trip_id = str(uuid4())
                trip_data = {
                    "trip_id": trip_id,
                    "toy_id": toy_id,
                    "toy_name": toy_name,
                    "title": trip.trip_title,
                    "description": trip.trip_description,
                    "location_name": trip.location_name,
                    "country_code": trip.country_code,
                    "gallery_images": [],
                }

                # Generate gallery images
                print(f"   🖼️  Generating gallery images...")

                num_images = random.randint(
                    config["min_images_per_trip"], config["max_images_per_trip"]
                )

                print(f"      📍 Generating {num_images} image(s) from {destination.location_name}")

                # Generate prompts
                prompts = generate_gallery_prompts(
                    client,
                    config["gpt_model"],
                    toy_name,
                    destination.location_name,
                    destination.famous_landmarks,
                    num_images,
                )

                # Execute image generation in parallel
                print(f"      🚀 Generating {len(prompts)} images in parallel...")
                with ThreadPoolExecutor(max_workers=min(num_images, 5)) as executor:
                    futures = {
                        executor.submit(
                            generate_single_image_task,
                            client,
                            config["image_model"],
                            toy_name,
                            toy_description,
                            prompt_obj,
                            1,  # All images are for single destination
                            images_dir,
                        ): prompt_obj for prompt_obj in prompts
                    }

                    for future in as_completed(futures):
                        prompt_obj = futures[future]
                        
                        result = future.result()
                        if result:
                            trip_data["gallery_images"].append(result)
                            print(f"         ✅ {prompt_obj.landmark}")

                print(
                    f"   ✅ Generated {len(trip_data['gallery_images'])} gallery images"
                )

                # Validate trip has images before saving
                if not trip_data["gallery_images"]:
                    print(f"   ⚠️  No images generated - skipping trip to {trip.location_name}")
                    continue

                # Add trip to collection
                all_trips.append(trip_data)

                # Save incrementally
                save_trips(output_file, all_trips)

        # Final summary
        print()
        print("=" * 70)
        print("📊 Generation Summary")
        print(f"   Total trips: {len(all_trips)}")
        print(f"   New trips: {len(all_trips) - len(existing_trips)}")
        total_images = sum(len(t.get("gallery_images", [])) for t in all_trips)
        print(f"   Total gallery images: {total_images}")
        print()
        print("✨ Trip generation complete!")
        print(f"   Trips saved to: {output_file}")
        print(f"   Images saved to: {images_dir}")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        print("   Partial results saved")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
