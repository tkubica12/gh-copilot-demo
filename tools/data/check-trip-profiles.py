"""
Check trip profiles in the trip service.

This script:
1. Lists all trips
2. Downloads gallery images to verify they work (doesn't save)
3. Prints summary

Requires:
- TRIP_SERVICE_URL environment variable
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


def format_bytes(size: int) -> str:
    """Format byte size as human-readable string."""
    for unit in ["B", "KB", "MB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} GB"


def main():
    """Check trip profiles and gallery images."""
    print("🔍 Trip Profile Check")
    print("=" * 50)

    # Load configuration
    service_url = os.getenv("TRIP_SERVICE_URL", "http://localhost:8002")
    print(f"📡 Service URL: {service_url}")

    print()

    # List all trips
    print("📋 Fetching trip list...")
    try:
        # Use a high limit to get all trips
        response = httpx.get(
            f"{service_url}/trip",
            params={"limit": 1000},
            timeout=10.0,
        )
        response.raise_for_status()
        response_data = response.json()
        trips = response_data.get("items", [])
        total = response_data.get("total", len(trips))
        print(f"✅ Found {len(trips)} trips (total in database: {total})")
    except httpx.HTTPError as e:
        print(f"❌ Failed to fetch trips: {e}")
        sys.exit(1)

    if not trips:
        print("\n✨ No trips found")
        return

    print()
    print("🗺️  Trip Profiles")
    print("-" * 50)

    # Check each trip and gallery images
    image_ok = 0
    image_missing = 0
    image_failed = 0
    total_legs = 0
    total_images = 0

    for idx, trip in enumerate(trips, 1):
        trip_id = trip["id"]
        trip_title = trip["title"]
        owner_oid = trip.get("owner_oid", "unknown")
        toy_id = trip.get("toy_id", "unknown")
        legs = trip.get("legs", [])
        gallery = trip.get("gallery", [])

        total_legs += len(legs)
        total_images += len(gallery)

        print(f"\n[{idx}] {trip_title}")
        print(f"    ID: {trip_id}")
        print(f"    Toy ID: {toy_id}")
        print(f"    Owner: {owner_oid[:8]}...")
        print(f"    Legs: {len(legs)}")

        # List legs
        for leg in legs[:3]:  # Show first 3 legs
            print(
                f"       {leg['leg_number']}. {leg['location_name']}, {leg['country_code']}"
            )
        if len(legs) > 3:
            print(f"       ... and {len(legs) - 3} more")

        print(f"    Gallery: {len(gallery)} images")

        # Check gallery images
        if gallery:
            checked_images = 0
            for image in gallery[:3]:  # Check first 3 images
                image_id = image["image_id"]
                try:
                    response = httpx.get(
                        f"{service_url}/trip/{trip_id}/gallery/{image_id}",
                        timeout=10.0,
                    )
                    response.raise_for_status()

                    content_type = response.headers.get("content-type", "unknown")
                    content_length = len(response.content)
                    image_ok += 1
                    checked_images += 1
                except httpx.HTTPError:
                    image_failed += 1
                except Exception:
                    image_failed += 1

            if checked_images > 0:
                print(f"       ✅ Checked {checked_images} images - all OK")
            if len(gallery) > 3:
                print(f"       ... and {len(gallery) - 3} more images")
        else:
            image_missing += 1

    # Summary
    print()
    print("=" * 50)
    print("📊 Summary")
    print(f"   Total trips: {len(trips)}")
    print(f"   Total legs: {total_legs}")
    print(f"   Total images: {total_images}")
    print(f"   Images checked: {image_ok}")
    print(f"   Images failed: {image_failed}")
    print()

    if image_failed == 0:
        print("✨ All checks passed!")
    else:
        print(f"⚠️  {image_failed} image(s) failed to load")


if __name__ == "__main__":
    main()
