import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_refresh(client):
    email = "testuser@example.com"
    activity = "Chess Club"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]


def test_unregister_participant(client):
    activity = "Chess Club"
    email = "toremove@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert email not in activities[activity]["participants"]
