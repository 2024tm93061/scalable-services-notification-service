import os
import pytest
import requests

# Use BASE_URL to point tests at a running instance (e.g. Docker container).
# Default is the local dev server used in the README.
BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture(scope="session", autouse=True)
def check_server_available():
    """Skip the tests if the target server is not reachable.

    This allows the same test file to be used for local TestClient-based
    testing or for integration testing against a running Docker container.
    """
    try:
        requests.get(f"{BASE}/docs", timeout=2)
    except requests.exceptions.RequestException:
        pytest.skip(f"Server not available at {BASE}; skipping integration tests")


def post_notify(payload):
    return requests.post(f"{BASE}/notify", json=payload)


def test_notify_email():
    res = post_notify({"email": "alice@example.com", "message": "Hello Alice"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    # masked email should not reveal full local-part
    assert data["sent_to"] != "alice@example.com"
    assert "@" in data["sent_to"]


def test_notify_phone():
    res = post_notify({"phone": "+1-555-123-4567", "message": "Hi there"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["sent_to"].startswith("*") or data["sent_to"].isdigit()


def test_missing_target():
    res = post_notify({"message": "No target"})
    assert res.status_code == 400
