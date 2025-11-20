"""
Clean all toy profiles from the toy service.

This script:
1. Lists all toys
2. Deletes all avatars
3. Deletes all toys

Requires:
- TOY_SERVICE_URL environment variable
- Running toy service
"""

import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def main():
    """Clean all toy profiles."""
    print("🧹 Toy Profile Cleanup")
    print("=" * 50)
    
    # Load configuration
    service_url = os.getenv("TOY_SERVICE_URL", "http://localhost:8001")
    print(f"📡 Service URL: {service_url}")
    
    print()
    
    # List all toys
    print("📋 Fetching toy list...")
    try:
        response = httpx.get(f"{service_url}/toy", timeout=10.0)
        response.raise_for_status()
        response_data = response.json()
        all_toys = response_data.get("items", [])
        print(f"✅ Found {len(all_toys)} total toys")
    except httpx.HTTPError as e:
        print(f"❌ Failed to fetch toys: {e}")
        sys.exit(1)
    
    toys_to_delete = all_toys
    
    print(f"🎯 {len(toys_to_delete)} toys will be deleted")
    
    if not toys_to_delete:
        print("\n✨ No toys to clean (database is empty)")
        return
    
    print()
    
    # Delete avatars first
    print("🖼️  Deleting avatars...")
    avatar_deleted = 0
    avatar_skipped = 0
    avatar_failed = 0
    
    for toy in toys_to_delete:
        toy_id = toy["id"]
        toy_name = toy["name"]
        has_avatar = toy.get("has_avatar", False)
        
        if not has_avatar:
            print(f"   ⏭️  {toy_name} (no avatar)")
            avatar_skipped += 1
            continue
        
        try:
            response = httpx.delete(
                f"{service_url}/toy/{toy_id}/avatar",
                timeout=10.0
            )
            if response.status_code == 204:
                print(f"   ✅ {toy_name}")
                avatar_deleted += 1
            else:
                print(f"   ⚠️  {toy_name} (status {response.status_code})")
                avatar_failed += 1
        except Exception as e:
            print(f"   ❌ {toy_name}: {e}")
            avatar_failed += 1
    
    print(f"\n📊 Avatars: {avatar_deleted} deleted, {avatar_skipped} skipped, {avatar_failed} failed")
    print()
    
    # Delete toys
    print("🧸 Deleting toys...")
    toy_deleted = 0
    toy_failed = 0
    
    for toy in toys_to_delete:
        toy_id = toy["id"]
        toy_name = toy["name"]
        
        try:
            response = httpx.delete(
                f"{service_url}/toy/{toy_id}",
                timeout=10.0
            )
            if response.status_code == 204:
                print(f"   ✅ {toy_name}")
                toy_deleted += 1
            else:
                print(f"   ⚠️  {toy_name} (status {response.status_code})")
                toy_failed += 1
        except Exception as e:
            print(f"   ❌ {toy_name}: {e}")
            toy_failed += 1
    
    print(f"\n📊 Toys: {toy_deleted} deleted, {toy_failed} failed")
    print()
    
    # Summary
    if toy_failed == 0:
        print("✨ Cleanup complete!")
    else:
        print(f"⚠️  Cleanup complete with {toy_failed} failures")


if __name__ == "__main__":
    main()
