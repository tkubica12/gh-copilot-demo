"""
Integration tests for Trip Service with real authentication.

These tests use real Azure resources (Cosmos DB, Blob Storage) and real 
authentication tokens. They verify the complete end-to-end flow including:
- Token validation
- Ownership checks (via toy service)
- Database operations
- Blob storage operations (gallery images)

Prerequisites:
1. Run: python tools/identity/create_app_registration.py
2. Run: python tools/identity/get_auth_token.py
3. Start toy service: cd src/services/toy && uv run python main.py
4. Start trip service: cd src/services/trip && uv run python main.py
5. Set environment: TRIP_SERVICE_URL=http://localhost:8002
"""

from datetime import datetime, UTC
from io import BytesIO

import httpx
import pytest


@pytest.mark.integration
@pytest.mark.auth
class TestTripServiceAuthentication:
    """Test trip service with real authentication and authorization."""

    @pytest.fixture
    def test_toy_id(self, service_config: dict, auth_headers: dict, cleanup_toys: list) -> str:
        """Create a test toy for trip tests."""
        base_url = service_config["toy_service_url"]
        toy_data = {"name": "Trip Test Toy", "description": "Toy for trip integration tests"}

        response = httpx.post(f"{base_url}/toy", json=toy_data, headers=auth_headers, timeout=10.0)
        assert response.status_code == 201

        toy = response.json()
        toy_id = toy["id"]
        cleanup_toys.append(toy_id)

        return toy_id

    @pytest.fixture
    def cleanup_trips(self, service_config: dict, auth_headers: dict):
        """Cleanup fixture to delete trips after tests."""
        trip_ids = []
        yield trip_ids

        # Cleanup trips
        base_url = service_config.get("trip_service_url", "http://localhost:8002")
        for trip_id in trip_ids:
            try:
                httpx.delete(f"{base_url}/trip/{trip_id}", headers=auth_headers, timeout=10.0)
            except Exception:  # noqa: S110
                pass  # Ignore cleanup failures

    @pytest.mark.usefixtures("check_services_available")
    def test_create_and_get_trip(
        self, service_config: dict, auth_headers: dict, test_toy_id: str, cleanup_trips: list, user_oid: str
    ):
        """Test creating and retrieving a trip with real auth."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create trip
        trip_data = {
            "toy_id": test_toy_id,
            "title": "European Adventure",
            "description": "A grand tour of Europe",
            "location_name": "Paris",
            "country_code": "FR",
            "public_tracking_enabled": False,
        }

        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)

        assert response.status_code == 201, f"Failed to create trip: {response.text}"
        trip = response.json()

        assert trip["title"] == "European Adventure"
        assert trip["toy_id"] == test_toy_id
        assert trip["owner_oid"] == user_oid  # Denormalized from toy
        assert trip["location_name"] == "Paris"
        assert trip["country_code"] == "FR"  # Validated to uppercase

        trip_id = trip["id"]
        cleanup_trips.append(trip_id)

        # Get trip
        response = httpx.get(f"{base_url}/trip/{trip_id}", headers=auth_headers, timeout=10.0)

        assert response.status_code == 200
        retrieved_trip = response.json()
        assert retrieved_trip["id"] == trip_id
        assert retrieved_trip["title"] == "European Adventure"
        assert retrieved_trip["location_name"] == "Paris"

    @pytest.mark.usefixtures("check_services_available")
    def test_create_trip_requires_toy_ownership(
        self, service_config: dict, auth_headers: dict, cleanup_trips: list
    ):
        """Test that creating a trip requires owning the toy."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Try to create trip with non-existent toy
        trip_data = {
            "toy_id": "00000000-0000-0000-0000-000000000000",
            "title": "Unauthorized Trip",
            "location_name": "Nowhere",
            "country_code": "XX",
        }

        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)

        # Should fail because toy doesn't exist or we don't own it
        assert response.status_code in (403, 404), f"Should reject unauthorized trip: {response.text}"

    @pytest.mark.usefixtures("check_services_available")
    def test_authentication_required(self, service_config: dict, test_toy_id: str):
        """Test that endpoints require authentication."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Try to create trip without auth
        trip_data = {
            "toy_id": test_toy_id,
            "title": "Unauthorized Trip",
            "location_name": "Nowhere",
            "country_code": "XX",
        }
        response = httpx.post(f"{base_url}/trip", json=trip_data, timeout=10.0)

        assert response.status_code == 401, "Should require authentication"

    @pytest.mark.usefixtures("check_services_available")
    def test_update_trip(
        self, service_config: dict, auth_headers: dict, test_toy_id: str, cleanup_trips: list
    ):
        """Test updating a trip with real auth."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create trip
        trip_data = {
            "toy_id": test_toy_id,
            "title": "Original Title",
            "location_name": "Berlin",
            "country_code": "DE",
        }
        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)
        trip_id = response.json()["id"]
        cleanup_trips.append(trip_id)

        # Update trip
        update_data = {"title": "Updated Title", "description": "Updated by integration test"}
        response = httpx.patch(f"{base_url}/trip/{trip_id}", json=update_data, headers=auth_headers, timeout=10.0)

        assert response.status_code == 200
        updated_trip = response.json()
        assert updated_trip["title"] == "Updated Title"
        assert updated_trip["description"] == "Updated by integration test"

    @pytest.mark.usefixtures("check_services_available")
    def test_list_trips_by_toy(
        self, service_config: dict, auth_headers: dict, test_toy_id: str, cleanup_trips: list
    ):
        """Test listing trips filtered by toy."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create trips
        trip_ids = []
        for i in range(2):
            trip_data = {
                "toy_id": test_toy_id,
                "title": f"Trip {i}",
                "location_name": f"City {i}",
                "country_code": "US",
            }
            response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)
            trip_ids.append(response.json()["id"])

        cleanup_trips.extend(trip_ids)

        # List trips by toy
        response = httpx.get(f"{base_url}/trip?toy_id={test_toy_id}", headers=auth_headers, timeout=10.0)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) >= 2
        assert all(trip["toy_id"] == test_toy_id for trip in data["items"])

    @pytest.mark.usefixtures("check_services_available")
    def test_list_trips_by_owner(
        self, service_config: dict, auth_headers: dict, test_toy_id: str, cleanup_trips: list, user_oid: str
    ):
        """Test listing trips filtered by owner."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create trip
        trip_data = {
            "toy_id": test_toy_id,
            "title": "Owner Filter Test",
            "location_name": "Seattle",
            "country_code": "US",
        }
        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)
        cleanup_trips.append(response.json()["id"])

        # List trips by owner
        response = httpx.get(f"{base_url}/trip?owner_oid={user_oid}", headers=auth_headers, timeout=10.0)

        assert response.status_code == 200
        data = response.json()
        assert all(trip["owner_oid"] == user_oid for trip in data["items"])

    @pytest.mark.usefixtures("check_services_available")
    def test_delete_trip(
        self, service_config: dict, auth_headers: dict, test_toy_id: str
    ):
        """Test deleting a trip with real auth."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create trip
        trip_data = {
            "toy_id": test_toy_id,
            "title": "To Delete",
            "location_name": "London",
            "country_code": "GB",
        }
        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)
        trip_id = response.json()["id"]

        # Delete trip
        response = httpx.delete(f"{base_url}/trip/{trip_id}", headers=auth_headers, timeout=10.0)

        assert response.status_code == 204

        # Verify deleted
        response = httpx.get(f"{base_url}/trip/{trip_id}", headers=auth_headers, timeout=10.0)
        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.auth
class TestTripGallery:
    """Test gallery image operations."""

    @pytest.fixture
    def test_toy_id(self, service_config: dict, auth_headers: dict, cleanup_toys: list) -> str:
        """Create a test toy for gallery tests."""
        base_url = service_config["toy_service_url"]
        response = httpx.post(
            f"{base_url}/toy", json={"name": "Gallery Test Toy"}, headers=auth_headers, timeout=10.0
        )
        toy_id = response.json()["id"]
        cleanup_toys.append(toy_id)
        return toy_id

    @pytest.fixture
    def test_trip_id(
        self, service_config: dict, auth_headers: dict, test_toy_id: str, cleanup_trips: list
    ) -> str:
        """Create a test trip for gallery tests."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")
        trip_data = {
            "toy_id": test_toy_id,
            "title": "Gallery Test Trip",
            "location_name": "Prague",
            "country_code": "CZ",
        }
        response = httpx.post(f"{base_url}/trip", json=trip_data, headers=auth_headers, timeout=10.0)
        trip_id = response.json()["id"]
        cleanup_trips.append(trip_id)
        return trip_id

    @pytest.fixture
    def cleanup_trips(self, service_config: dict, auth_headers: dict):
        """Cleanup fixture for trips."""
        trip_ids = []
        yield trip_ids
        base_url = service_config.get("trip_service_url", "http://localhost:8002")
        for trip_id in trip_ids:
            try:
                httpx.delete(f"{base_url}/trip/{trip_id}", headers=auth_headers, timeout=10.0)
            except Exception:  # noqa: S110
                pass

    @pytest.mark.usefixtures("check_services_available")
    def test_upload_and_get_gallery_image(
        self, service_config: dict, auth_headers: dict, test_trip_id: str
    ):
        """Test uploading and retrieving a gallery image."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Create a fake image (1x1 pixel JPEG)
        fake_image = BytesIO(
            b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
            b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c"
        )
        fake_image.name = "test_image.jpg"

        # Upload image
        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        params = {"landmark": "Test Landmark", "caption": "Test gallery image"}

        # For file uploads, only include Authorization header (not Content-Type)
        upload_headers = {"Authorization": auth_headers["Authorization"]}
        
        response = httpx.post(
            f"{base_url}/trip/{test_trip_id}/gallery",
            files=files,
            params=params,
            headers=upload_headers,
            timeout=10.0,
        )

        assert response.status_code == 200, f"Failed to upload image: {response.text}"
        trip = response.json()
        assert len(trip["gallery"]) == 1
        assert trip["gallery"][0]["landmark"] == "Test Landmark"
        assert trip["gallery"][0]["caption"] == "Test gallery image"

        image_id = trip["gallery"][0]["image_id"]

        # Download image
        response = httpx.get(
            f"{base_url}/trip/{test_trip_id}/gallery/{image_id}", headers=auth_headers, timeout=10.0
        )

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/")
        assert "cache-control" in response.headers

    @pytest.mark.usefixtures("check_services_available")
    def test_delete_gallery_image(
        self, service_config: dict, auth_headers: dict, test_trip_id: str
    ):
        """Test deleting a gallery image."""
        base_url = service_config.get("trip_service_url", "http://localhost:8002")

        # Upload image
        fake_image = BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
        files = {"file": ("test.jpg", fake_image, "image/jpeg")}
        params = {"landmark": "Test Landmark"}

        # For file uploads, only include Authorization header (not Content-Type)
        upload_headers = {"Authorization": auth_headers["Authorization"]}
        
        response = httpx.post(
            f"{base_url}/trip/{test_trip_id}/gallery",
            files=files,
            params=params,
            headers=upload_headers,
            timeout=10.0,
        )
        image_id = response.json()["gallery"][0]["image_id"]

        # Delete image
        response = httpx.delete(
            f"{base_url}/trip/{test_trip_id}/gallery/{image_id}", headers=auth_headers, timeout=10.0
        )

        assert response.status_code == 204

        # Verify image removed from trip
        response = httpx.get(f"{base_url}/trip/{test_trip_id}", headers=auth_headers, timeout=10.0)
        trip = response.json()
        assert len(trip["gallery"]) == 0



