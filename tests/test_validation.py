import pytest


def test_signup_missing_email(client):
    """Test signup with missing email parameter"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity
    error_detail = response.json()
    assert "email" in str(error_detail)  # FastAPI validation error


def test_signup_empty_email(client):
    """Test signup with empty email string"""
    # Arrange
    activity_name = "Chess Club"
    email = ""

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200  # App accepts empty string
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_special_characters_email(client):
    """Test signup with email containing special characters"""
    # Arrange
    activity_name = "Programming Class"
    email = "test+special@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_unregister_missing_email(client):
    """Test unregister with missing email parameter"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity
    error_detail = response.json()
    assert "email" in str(error_detail)  # FastAPI validation error


def test_unregister_empty_email(client):
    """Test unregister with empty email string"""
    # Arrange
    activity_name = "Chess Club"
    email = ""

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400  # Not signed up
    assert "not signed up" in response.json()["detail"]


def test_signup_capacity_check(client):
    """Test signing up when activity is at max capacity"""
    # Arrange - Find an activity and fill it to capacity
    activity_name = "Tennis Club"  # max_participants: 10
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Fill to capacity
    for i in range(10 - initial_count):
        email = f"student{i}@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Now try to add one more
    extra_email = "extra@student.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": extra_email})

    # Assert - The app doesn't check capacity, so it allows
    # Based on code, no capacity check, so it succeeds
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {extra_email} for {activity_name}"}