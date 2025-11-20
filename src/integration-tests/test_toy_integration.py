"""
Integration tests for Toy Service with real authentication.

These tests use real Azure resources (Cosmos DB, Blob Storage) and real 
authentication tokens. They verify the complete end-to-end flow including:
- Token validation
- Ownership checks
- Database operations
- Blob storage operations

Prerequisites:
1. Run: python tools/identity/create_app_registration.py
2. Run: python tools/identity/get_auth_token.py
3. Start toy service: cd src/services/toy && uv run uvicorn main:app --reload
4. Set environment: TOY_SERVICE_URL=http://localhost:8000
"""

from io import BytesIO

import httpx
import pytest


@pytest.mark.integration
@pytest.mark.auth
class TestToyServiceAuthentication:
    """Test toy service with real authentication and authorization."""

    @pytest.mark.usefixtures("check_services_available")
    def test_create_and_get_toy(
        self, service_config: dict, auth_headers: dict, cleanup_toys: list, user_oid: str
    ):
        """Test creating and retrieving a toy with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create toy
        toy_data = {
            "name": "Integration Test Teddy",
            "description": "Created by integration test with real auth"
        }
        
        response = httpx.post(f"{base_url}/toy", json=toy_data, headers=auth_headers, timeout=10.0)
        
        assert response.status_code == 201, f"Failed to create toy: {response.text}"
        toy = response.json()
        
        assert toy["name"] == "Integration Test Teddy"
        assert toy["owner_oid"] == user_oid  # Verify owner from token
        assert toy["has_avatar"] is False
        
        toy_id = toy["id"]
        cleanup_toys.append(toy_id)
        
        # Get toy
        response = httpx.get(f"{base_url}/toy/{toy_id}", headers=auth_headers, timeout=10.0)
        
        assert response.status_code == 200
        retrieved_toy = response.json()
        assert retrieved_toy["id"] == toy_id
        assert retrieved_toy["name"] == "Integration Test Teddy"

    @pytest.mark.usefixtures("check_services_available")
    def test_authentication_required(self, service_config: dict):
        """Test that endpoints require authentication."""
        base_url = service_config["toy_service_url"]
        
        # Try to create toy without auth
        toy_data = {"name": "Unauthorized Toy"}
        response = httpx.post(f"{base_url}/toy", json=toy_data, timeout=10.0)
        
        assert response.status_code == 401, "Should require authentication"

    @pytest.mark.usefixtures("check_services_available")
    def test_update_toy(
        self, service_config: dict, auth_headers: dict, cleanup_toys: list
    ):
        """Test updating a toy with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create toy
        toy_data = {"name": "Original Name"}
        response = httpx.post(f"{base_url}/toy", json=toy_data, headers=auth_headers, timeout=10.0)
        toy_id = response.json()["id"]
        cleanup_toys.append(toy_id)
        
        # Update toy
        update_data = {
            "name": "Updated Name",
            "description": "Updated by integration test"
        }
        response = httpx.patch(
            f"{base_url}/toy/{toy_id}", json=update_data, headers=auth_headers, timeout=10.0
        )
        
        assert response.status_code == 200
        updated_toy = response.json()
        assert updated_toy["name"] == "Updated Name"
        assert updated_toy["description"] == "Updated by integration test"

    @pytest.mark.usefixtures("check_services_available")
    def test_list_toys(
        self, service_config: dict, auth_headers: dict, cleanup_toys: list, user_oid: str
    ):
        """Test listing toys with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create a few toys
        toy_ids = []
        for i in range(3):
            response = httpx.post(
                f"{base_url}/toy",
                json={"name": f"List Test Toy {i}"},
                headers=auth_headers,
                timeout=10.0
            )
            toy_ids.append(response.json()["id"])
        
        cleanup_toys.extend(toy_ids)
        
        # List all toys
        response = httpx.get(f"{base_url}/toy", headers=auth_headers, timeout=10.0)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) >= 3
        
        # Filter by owner
        response = httpx.get(
            f"{base_url}/toy?owner_oid={user_oid}", headers=auth_headers, timeout=10.0
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(toy["owner_oid"] == user_oid for toy in data["items"])

    @pytest.mark.usefixtures("check_services_available")
    def test_delete_toy(
        self, service_config: dict, auth_headers: dict
    ):
        """Test deleting a toy with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create toy
        response = httpx.post(
            f"{base_url}/toy",
            json={"name": "To Delete"},
            headers=auth_headers,
            timeout=10.0
        )
        toy_id = response.json()["id"]
        
        # Delete toy
        response = httpx.delete(f"{base_url}/toy/{toy_id}", headers=auth_headers, timeout=10.0)
        assert response.status_code == 204
        
        # Verify deleted
        response = httpx.get(f"{base_url}/toy/{toy_id}", headers=auth_headers, timeout=10.0)
        assert response.status_code == 404

    @pytest.mark.usefixtures("check_services_available")
    def test_upload_and_get_avatar(
        self, service_config: dict, auth_headers: dict, cleanup_toys: list
    ):
        """Test uploading and retrieving an avatar with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create toy
        response = httpx.post(
            f"{base_url}/toy",
            json={"name": "Avatar Test Toy"},
            headers=auth_headers,
            timeout=10.0
        )
        toy_id = response.json()["id"]
        cleanup_toys.append(toy_id)
        
        # Create a fake image file
        fake_image_content = b"fake image content for testing"
        files = {
            "file": ("avatar.jpg", BytesIO(fake_image_content), "image/jpeg")
        }
        
        # Upload avatar (multipart, so remove Content-Type header)
        upload_headers = {k: v for k, v in auth_headers.items() if k != "Content-Type"}
        response = httpx.post(
            f"{base_url}/toy/{toy_id}/avatar",
            files=files,
            headers=upload_headers,
            timeout=10.0
        )
        
        assert response.status_code == 200
        updated_toy = response.json()
        assert updated_toy["has_avatar"] is True
        assert updated_toy["avatar_blob_name"] is not None
        
        # Get avatar
        response = httpx.get(
            f"{base_url}/toy/{toy_id}/avatar", headers=auth_headers, timeout=10.0
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
        assert "cache-control" in response.headers

    @pytest.mark.usefixtures("check_services_available")
    def test_delete_avatar(
        self, service_config: dict, auth_headers: dict, cleanup_toys: list
    ):
        """Test deleting an avatar with real auth."""
        base_url = service_config["toy_service_url"]
        
        # Create toy with avatar
        response = httpx.post(
            f"{base_url}/toy",
            json={"name": "Avatar Delete Test"},
            headers=auth_headers,
            timeout=10.0
        )
        toy_id = response.json()["id"]
        cleanup_toys.append(toy_id)
        
        # Upload avatar
        files = {"file": ("avatar.jpg", BytesIO(b"fake image"), "image/jpeg")}
        upload_headers = {k: v for k, v in auth_headers.items() if k != "Content-Type"}
        httpx.post(
            f"{base_url}/toy/{toy_id}/avatar",
            files=files,
            headers=upload_headers,
            timeout=10.0
        )
        
        # Delete avatar
        response = httpx.delete(
            f"{base_url}/toy/{toy_id}/avatar", headers=auth_headers, timeout=10.0
        )
        assert response.status_code == 204
        
        # Verify avatar deleted
        response = httpx.get(f"{base_url}/toy/{toy_id}", headers=auth_headers, timeout=10.0)
        toy = response.json()
        assert toy["has_avatar"] is False
        assert toy["avatar_blob_name"] is None


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.slow
class TestToyServiceOwnership:
    """Test ownership-based authorization (requires second user token)."""

    def test_ownership_enforcement(self, service_config: dict, auth_headers: dict):
        """
        Test that only owners can modify toys.
        
        Note: This test is limited because we only have one user token.
        In a full test environment, you'd create a second app user and token.
        For now, we verify the owner check exists by confirming successful operations
        on owned toys.
        """
        base_url = service_config["toy_service_url"]
        
        # Create toy (which we own)
        response = httpx.post(
            f"{base_url}/toy",
            json={"name": "Ownership Test"},
            headers=auth_headers,
            timeout=10.0
        )
        toy_id = response.json()["id"]
        
        try:
            # Verify we CAN modify our own toy
            response = httpx.patch(
                f"{base_url}/toy/{toy_id}",
                json={"name": "Modified by Owner"},
                headers=auth_headers,
                timeout=10.0
            )
            assert response.status_code == 200, "Owner should be able to modify toy"
            
            # TODO: To fully test ownership, create a second user's token
            # and verify they CANNOT modify this toy (expect 403)
            
        finally:
            # Cleanup
            httpx.delete(f"{base_url}/toy/{toy_id}", headers=auth_headers, timeout=10.0)
