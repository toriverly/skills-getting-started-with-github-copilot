from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def restore_activity_state():
    original_activities = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_activities))


def test_signup_for_activity_returns_success_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
        timeout=5,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_unregister_participant_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}", timeout=5)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        timeout=5,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_signup_returns_error_for_existing_student(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}",
        timeout=5,
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
