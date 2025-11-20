"""
Import trip profiles from JSON into the trip service.

This script:
1. Reads trip profiles from JSON file
2. Creates trips via API (single destination per trip)
3. Uploads gallery images from images folder

Requires:
- TRIP_SERVICE_URL environment variable
- TRIP_PROFILES_JSON (default: trips.json)
- TRIP_IMAGES_FOLDER (default: trip-images)
- Running trip service
"""
import json
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def get_headers() -> dict:
    """Generate headers."""
    return {
        "Content-Type": "application/json",
    }


def main():
    """Import trip profiles from JSON."""
    print("📦 Trip Profile Import")
    print("=" * 50)

    # Load configuration
    service_url = os.getenv("TRIP_SERVICE_URL", "http://localhost:8002")
    profiles_file = os.getenv("TRIP_PROFILES_JSON", "trips.json")
    images_folder = os.getenv("TRIP_IMAGES_FOLDER", "trip-images")

    print(f"📡 Service URL: {service_url}")
    print(f"📄 Profiles file: {profiles_file}")
    print(f"🖼️  Images folder: {images_folder}")

    # Resolve paths
    profiles_path = Path(__file__).parent / profiles_file
    images_path = Path(__file__).parent / images_folder

    # Validate files exist
    if not profiles_path.exists():
        print(f"\n❌ Profiles file not found: {profiles_path}")
        sys.exit(1)

    if not images_path.exists() or not images_path.is_dir():
        print(f"\n❌ Images folder not found: {images_path}")
        sys.exit(1)

    headers = get_headers()

    # Load profiles
    try:
        with open(profiles_path, encoding="utf-8") as f:
            profiles = json.load(f)
        print(f"✅ Loaded {len(profiles)} trip profiles")
    except Exception as e:
        print(f"❌ Failed to load profiles: {e}")
        sys.exit(1)

    print()

    # Import trips
    print("🗺️  Creating trips...")
    created = 0
    failed = 0
    image_uploaded = 0
    image_failed = 0

    for idx, profile in enumerate(profiles, 1):
        trip_title = profile.get("title", "Unknown")
        toy_name = profile.get("toy_name", "Unknown")
        gallery_images = profile.get("gallery_images", [])

        print(f"\n[{idx}/{len(profiles)}] {trip_title}")
        print(f"   Toy: {toy_name}")

        # Create trip
        trip_data = {
            "toy_id": profile["toy_id"],
            "title": profile["title"],
            "description": profile.get("description", ""),
            "location_name": profile["location_name"],
            "country_code": profile["country_code"],
        }

        try:
            response = httpx.post(
                f"{service_url}/trip", json=trip_data, headers=headers, timeout=30.0
            )
            response.raise_for_status()
            trip = response.json()
            trip_id = trip["id"]
            print(f"   ✅ Created trip (ID: {trip_id})")
            print(f"      Location: {profile['location_name']}, {profile['country_code']}")
            created += 1
        except httpx.HTTPError as e:
            print(f"   ❌ Failed to create trip: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"      Response: {e.response.text}")
            failed += 1
            continue
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            failed += 1
            continue

        # Upload gallery images if available
        if gallery_images:
            print(f"   🖼️  Uploading {len(gallery_images)} gallery images...")

            for img_idx, image_meta in enumerate(gallery_images, 1):
                blob_name = image_meta["blob_name"]
                landmark = image_meta.get("landmark", "")
                caption = image_meta.get("caption", "")

                image_file = images_path / blob_name

                if not image_file.exists():
                    print(f"      ⚠️  Image not found: {blob_name}")
                    image_failed += 1
                    continue

                try:
                    with open(image_file, "rb") as img:
                        files = {"file": (blob_name, img, "image/jpeg")}
                        data = {}
                        if landmark:
                            data["landmark"] = landmark
                        if caption:
                            data["caption"] = caption

                        # Remove Content-Type header for multipart
                        upload_headers = {
                            k: v
                            for k, v in headers.items()
                            if k.lower() != "content-type"
                        }

                        response = httpx.post(
                            f"{service_url}/trip/{trip_id}/gallery",
                            files=files,
                            data=data,
                            headers=upload_headers,
                            timeout=60.0,
                        )
                        response.raise_for_status()
                        print(
                            f"      [{img_idx}/{len(gallery_images)}] ✅ {blob_name}"
                        )
                        image_uploaded += 1

                except httpx.HTTPError as e:
                    print(f"      ❌ Failed to upload {blob_name}: {e}")
                    if hasattr(e, "response") and e.response is not None:
                        print(f"         Response: {e.response.text}")
                    image_failed += 1
                except Exception as e:
                    print(f"      ❌ Unexpected error uploading {blob_name}: {e}")
                    image_failed += 1

        else:
            print(f"   ⏭️  No gallery images to upload")

    # Summary
    print()
    print("=" * 50)
    print("📊 Import Summary")
    print(f"   Trips created: {created}")
    print(f"   Trips failed: {failed}")
    print(f"   Gallery images uploaded: {image_uploaded}")
    print(f"   Gallery images failed: {image_failed}")
    print()

    if failed == 0 and image_failed == 0:
        print("✨ Import complete!")
    else:
        print(f"⚠️  Import complete with errors")


if __name__ == "__main__":
    main()
