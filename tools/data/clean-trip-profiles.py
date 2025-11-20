"""
Clean all trip profiles from the trip service.

This script:
1. Lists all trips
2. Deletes all gallery images
3. Deletes all trips

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


def main():
    """Clean all trip profiles."""
    print("🧹 Trip Profile Cleanup")
    print("=" * 50)

    # Load configuration
    service_url = os.getenv("TRIP_SERVICE_URL", "http://localhost:8002")
    print(f"📡 Service URL: {service_url}")

    print()

    # List all trips
    print("📋 Fetching trip list...")
    try:
        response = httpx.get(
            f"{service_url}/trip", params={"limit": 1000}, timeout=10.0
        )
        response.raise_for_status()
        response_data = response.json()
        all_trips = response_data.get("items", [])
        print(f"✅ Found {len(all_trips)} total trips")
    except httpx.HTTPError as e:
        print(f"❌ Failed to fetch trips: {e}")
        sys.exit(1)

    trips_to_delete = all_trips

    print(f"🎯 {len(trips_to_delete)} trips will be deleted")

    if not trips_to_delete:
        print("\n✨ No trips to clean (database is empty)")
        return

    print()

    # Delete gallery images first
    print("🖼️  Deleting gallery images...")
    image_deleted = 0
    image_skipped = 0
    image_failed = 0

    for trip in trips_to_delete:
        trip_id = trip["id"]
        trip_title = trip["title"]
        gallery = trip.get("gallery", [])

        if not gallery:
            continue

        for image in gallery:
            image_id = image["image_id"]

            try:
                response = httpx.delete(
                    f"{service_url}/trip/{trip_id}/gallery/{image_id}",
                    timeout=10.0,
                )
                response.raise_for_status()
                print(
                    f"   ✅ Deleted image {image_id} from {trip_title}"
                )
                image_deleted += 1
            except Exception as e:
                print(f"   ❌ Failed to delete image: {e}")
                image_failed += 1

    print(
        f"\n📊 Gallery Images: {image_deleted} deleted, {image_skipped} skipped, {image_failed} failed"
    )
    print()

    # Delete trips
    print("🗺️  Deleting trips...")
    trip_deleted = 0
    trip_failed = 0

    for trip in trips_to_delete:
        trip_id = trip["id"]
        trip_title = trip["title"]

        try:
            response = httpx.delete(
                f"{service_url}/trip/{trip_id}", timeout=10.0
            )
            response.raise_for_status()
            print(f"   ✅ Deleted trip: {trip_title}")
            trip_deleted += 1
        except Exception as e:
            print(f"   ❌ Failed to delete trip {trip_title}: {e}")
            trip_failed += 1

    print(f"\n📊 Trips: {trip_deleted} deleted, {trip_failed} failed")
    print()

    # Summary
    if trip_failed == 0:
        print("✨ Cleanup complete!")
    else:
        print(f"⚠️  Cleanup complete with {trip_failed} failures")


if __name__ == "__main__":
    main()
