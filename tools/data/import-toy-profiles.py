"""
Import toy profiles from JSON into the toy service.

This script:
1. Reads toy profiles from JSON file
2. Creates toys via API
3. Uploads avatar images from images folder

Requires:
- TOY_SERVICE_URL environment variable
- TOY_PROFILES_JSON (default: toy_profiles.json)
- TOY_IMAGES_FOLDER (default: toy-images)
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


def get_headers() -> dict:
    """Generate headers."""
    return {
        "Content-Type": "application/json"
    }


def main():
    """Import toy profiles from JSON."""
    print("📦 Toy Profile Import")
    print("=" * 50)
    
    # Load configuration
    service_url = os.getenv("TOY_SERVICE_URL", "http://localhost:8001")
    profiles_file = os.getenv("TOY_PROFILES_JSON", "toy_profiles.json")
    images_folder = os.getenv("TOY_IMAGES_FOLDER", "toy-images")
    
    print(f"📡 Service URL: {service_url}")
    print(f"📄 Profiles file: {profiles_file}")
    print(f"🖼️ Images folder: {images_folder}")
    
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
        with open(profiles_path, encoding='utf-8') as f:
            profiles = json.load(f)
        print(f"✅ Loaded {len(profiles)} toy profiles")
    except Exception as e:
        print(f"❌ Failed to load profiles: {e}")
        sys.exit(1)
    
    print()
    
    # Import toys
    print("🧸 Creating toys...")
    created = 0
    failed = 0
    avatar_uploaded = 0
    avatar_failed = 0
    
    for idx, profile in enumerate(profiles, 1):
        toy_name = profile.get("name", "Unknown")
        toy_id = profile.get("id")
        avatar_blob_name = profile.get("avatar_blob_name")
        
        print(f"\n[{idx}/{len(profiles)}] {toy_name}")
        if toy_id:
            print(f"   Using explicit ID: {toy_id}")
        
        # Create toy
        toy_data = {
            "name": profile["name"],
            "description": profile.get("description", "")
        }
        
        # Include ID if present in profile
        if toy_id:
            toy_data["id"] = toy_id
        
        try:
            response = httpx.post(
                f"{service_url}/toy",
                json=toy_data,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            toy = response.json()
            toy_id = toy["id"]
            print(f"   ✅ Created toy (ID: {toy_id})")
            created += 1
        except httpx.HTTPError as e:
            print(f"   ❌ Failed to create toy: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"      Response: {e.response.text}")
            failed += 1
            continue
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            failed += 1
            continue
        
        # Upload avatar if available
        if avatar_blob_name:
            image_file = images_path / avatar_blob_name
            
            if not image_file.exists():
                print(f"   ⚠️  Avatar image not found: {avatar_blob_name}")
                avatar_failed += 1
                continue
            
            try:
                with open(image_file, "rb") as img:
                    files = {"file": (avatar_blob_name, img, "image/jpeg")}
                    
                    response = httpx.post(
                        f"{service_url}/toy/{toy_id}/avatar",
                        files=files,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    print(f"   ✅ Uploaded avatar: {avatar_blob_name}")
                    avatar_uploaded += 1
            except httpx.HTTPError as e:
                print(f"   ❌ Failed to upload avatar: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"      Response: {e.response.text}")
                avatar_failed += 1
            except Exception as e:
                print(f"   ❌ Unexpected error uploading avatar: {e}")
                avatar_failed += 1
        else:
            print(f"   ⏭️  No avatar specified")
    
    # Summary
    print()
    print("=" * 50)
    print("📊 Import Summary")
    print(f"   Toys created: {created}")
    print(f"   Toys failed: {failed}")
    print(f"   Avatars uploaded: {avatar_uploaded}")
    print(f"   Avatars failed: {avatar_failed}")
    print()
    
    if failed == 0 and avatar_failed == 0:
        print("✨ Import complete!")
    else:
        print(f"⚠️  Import complete with errors")


if __name__ == "__main__":
    main()
