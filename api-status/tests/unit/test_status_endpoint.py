"""Unit tests for status API endpoint.

Azure Cosmos dependency is faked; we verify both 200 and 202 paths.
"""

import sys


def test_status_returns_202_when_not_ready(client):
    resp = client.get("/api/status/some-guid")
    assert resp.status_code == 202
    assert resp.headers.get("Retry-After") == "5"
    assert resp.json()["message"].startswith("Processing")


def test_status_returns_200_when_item_present(monkeypatch, client):
    main = sys.modules["api_status_main"]  # loaded via conftest

    class FakeContainer:
        def query_items(self, query, parameters, partition_key):  # noqa: D401
            async def iterator():
                yield {"id": "abc", "ai_response": "result-data"}
            return iterator()

    monkeypatch.setattr(main, "container", FakeContainer())
    resp = client.get("/api/status/abc")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == "abc"
    assert body["data"]["result"] == "result-data"
