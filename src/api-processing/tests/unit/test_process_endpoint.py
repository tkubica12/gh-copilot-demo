"""Unit tests for the /api/process endpoint.

These tests mock Azure dependencies and only verify application logic & schema.
"""

import io
import sys


def test_process_image_returns_202_and_stores_blob(client):
    # Prepare in-memory image bytes (doesn't need to be a real JPEG for test)
    file_content = b"fake-image-data"
    response = client.post(
        "/api/process",
        files={"file": ("test.jpg", io.BytesIO(file_content), "image/jpeg")},
    )

    assert response.status_code == 202
    data = response.json()
    assert "id" in data and len(data["id"]) > 0
    assert data["results_url"].endswith(data["id"])  # URL pattern

    # Access faked uploaded blobs & queue messages
    main = sys.modules["api_processing_main"]  # loaded via conftest

    # One blob uploaded
    assert any(name.endswith(".jpg") for name in main._test_uploaded.keys())  # type: ignore[attr-defined]
    # One message sent containing the guid
    sent = main._test_queue.sent_messages  # type: ignore[attr-defined]
    assert len(sent) == 1
    # Since we parsed JSON into dict
    body = sent[0]
    assert isinstance(body, dict)
    assert body["id"] == data["id"]


def test_validation_error_when_file_missing(client):
    resp = client.post("/api/process")
    # FastAPI will produce 422 for missing file
    assert resp.status_code == 422
    body = resp.json()
    assert "detail" in body
