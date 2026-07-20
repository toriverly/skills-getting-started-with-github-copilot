from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}",
        timeout=5,
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}",
        timeout=5,
    )
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities", timeout=5)
    assert activities_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
