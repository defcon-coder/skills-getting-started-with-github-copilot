from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_activity_adds_participant():
    # Arrange
    activity = "Chess Club"
    email = "newstudent1@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    # Verify state changed
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activity = "Programming Class"
    email = "duplicate_student@mergington.edu"

    # Act
    first_response = client.post(f"/activities/{activity}/signup?email={email}")
    second_response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_remove_participant_from_activity():
    # Arrange
    activity = "Gym Class"
    email = "removestudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    # Act
    delete_response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_remove_nonexistent_participant_returns_404():
    # Arrange
    activity = "Drama Club"
    email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
