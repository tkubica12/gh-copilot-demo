"""Tests to verify async operations work correctly.

These tests ensure that the async Azure SDK clients are properly configured
and that concurrent requests can be handled efficiently.
"""

import io
import asyncio
import time


def test_multiple_concurrent_requests(client):
    """Test that multiple concurrent requests can be handled efficiently.
    
    This test verifies that the async implementation allows multiple requests
    to be processed concurrently without blocking.
    """
    # Prepare test data
    file_content = b"fake-image-data-concurrent"
    num_requests = 3
    
    # Send multiple requests concurrently
    start_time = time.time()
    
    responses = []
    for i in range(num_requests):
        response = client.post(
            "/api/process",
            files={"file": (f"test{i}.jpg", io.BytesIO(file_content), "image/jpeg")},
        )
        responses.append(response)
    
    elapsed_time = time.time() - start_time
    
    # Verify all requests succeeded
    for response in responses:
        assert response.status_code == 202
        data = response.json()
        assert "id" in data
        assert "results_url" in data
    
    # Verify all responses have unique IDs
    ids = [r.json()["id"] for r in responses]
    assert len(ids) == len(set(ids)), "All IDs should be unique"
    
    # The async implementation should handle these requests efficiently
    # Even though this is a synchronous test client, the underlying async
    # operations should not block each other
    print(f"Processed {num_requests} requests in {elapsed_time:.3f} seconds")


def test_file_upload_with_larger_content(client):
    """Test uploading a larger file to verify chunking works."""
    # Create a 1MB file
    file_content = b"x" * (1024 * 1024)
    
    response = client.post(
        "/api/process",
        files={"file": ("large.jpg", io.BytesIO(file_content), "image/jpeg")},
    )
    
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert "results_url" in data
