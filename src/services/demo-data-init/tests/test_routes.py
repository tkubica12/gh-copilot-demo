import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
SHARED_PATH = ROOT / "shared"
if str(SHARED_PATH) not in sys.path:
    sys.path.insert(0, str(SHARED_PATH))

from auth.models import AuthContext, Principal
from models import OperationSummary
from routes import router, configure_router
from routes import demo_data


class _StubImporter:
    def __init__(self, summary: OperationSummary | None = None, *, should_fail: bool = False):
        self.summary = summary or OperationSummary()
        self.should_fail = should_fail
        self.calls: list[tuple[bool, bool, str]] = []

    async def import_data(self, *, include_toys: bool, include_trips: bool, token: str) -> OperationSummary:
        self.calls.append((include_toys, include_trips, token))
        if self.should_fail:
            raise RuntimeError("boom")
        return self.summary


def _build_client(importer: _StubImporter, roles: list[str]) -> TestClient:
    configure_router(
        importer=importer,
        tenant_id="tenant",
        audience="audience",
        role_value="Admin.FullAccess",
    )
    app = FastAPI()
    app.include_router(router)

    principal = Principal(subject_id="user", roles=roles)
    auth_ctx = AuthContext(principal=principal)

    def auth_override(_: str | None = None) -> AuthContext:
        return auth_ctx

    app.dependency_overrides[demo_data.auth_dependency] = auth_override
    return TestClient(app)


def test_trigger_import_returns_summary():
    importer = _StubImporter(OperationSummary(toys_processed=3, trips_processed=1))
    client = _build_client(importer, roles=["Admin.FullAccess"])

    response = client.post(
        "/demo-data/import",
        json={"include_toys": True, "include_trips": False},
        headers={"Authorization": "Bearer fake"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["toys_processed"] == 3
    assert importer.calls == [(True, False, "fake")]


def test_trigger_import_requires_dataset_selection():
    importer = _StubImporter()
    client = _build_client(importer, roles=["Admin.FullAccess"])

    response = client.post(
        "/demo-data/import",
        json={"include_toys": False, "include_trips": False},
        headers={"Authorization": "Bearer fake"},
    )

    assert response.status_code == 400


def test_trigger_import_enforces_role():
    importer = _StubImporter()
    client = _build_client(importer, roles=["Other.Role"])

    response = client.post(
        "/demo-data/import",
        json={"include_toys": True, "include_trips": True},
        headers={"Authorization": "Bearer fake"},
    )

    assert response.status_code == 403


def test_trigger_import_propagates_errors():
    importer = _StubImporter(should_fail=True)
    client = _build_client(importer, roles=["Admin.FullAccess"])

    response = client.post(
        "/demo-data/import",
        json={"include_toys": True, "include_trips": True},
        headers={"Authorization": "Bearer fake"},
    )

    assert response.status_code == 502