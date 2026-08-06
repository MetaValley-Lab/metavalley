import os

os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "dummy-key")
os.environ.setdefault("IS_PRODUCTION", "false")

from fastapi.testclient import TestClient

from app.main import app


def test_auth_routes_are_registered():
    assert any(route.path == "/auth/login" for route in app.routes)
    assert any(route.path == "/auth/register" for route in app.routes)


def test_health_endpoint_is_available():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
