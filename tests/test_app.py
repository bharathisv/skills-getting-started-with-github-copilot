"""Tests for the Mergington High School Activities API."""

from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    """Reset test email before each test."""
    test_email = "pytest-test@mergington.edu"
    for activity in activities.values():
        if test_email in activity["participants"]:
            activity["participants"].remove(test_email)


def test_get_activities():
    """Test fetching all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    # Verify expected activities exist
    assert "Chess Club" in data
    assert "Tennis Club" in data


def test_activity_has_required_fields():
    """Test that each activity has required fields."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_new_participant():
    """Test signing up a new participant."""
    activity = "Chess Club"
    test_email = "pytest-test@mergington.edu"
    initial_count = len(activities[activity]["participants"])
    
    response = client.post(
        f"/activities/{activity}/signup?email={test_email}"
    )
    
    assert response.status_code == 200
    assert test_email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count + 1


def test_signup_duplicate_participant():
    """Test that duplicate signup returns error."""
    activity = "Tennis Club"
    test_email = "pytest-test@mergington.edu"
    
    # First signup
    response1 = client.post(
        f"/activities/{activity}/signup?email={test_email}"
    )
    assert response1.status_code == 200
    
    # Duplicate signup should fail
    response2 = client.post(
        f"/activities/{activity}/signup?email={test_email}"
    )
    assert response2.status_code == 400
    error = response2.json()
    assert "already signed up" in error["detail"].lower()


def test_signup_nonexistent_activity():
    """Test signing up for a nonexistent activity."""
    response = client.post(
        "/activities/FakeActivity/signup?email=test@example.com"
    )
    assert response.status_code == 404
    error = response.json()
    assert "not found" in error["detail"].lower()


def test_unregister_participant():
    """Test unregistering a participant."""
    activity = "Basketball Team"
    test_email = "pytest-test@mergington.edu"
    
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={test_email}")
    assert test_email in activities[activity]["participants"]
    initial_count = len(activities[activity]["participants"])
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/participants?email={test_email}"
    )
    assert response.status_code == 200
    assert test_email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count - 1


def test_unregister_nonexistent_participant():
    """Test unregistering a participant who isn't registered."""
    activity = "Art Club"
    fake_email = "nonexistent@example.com"
    
    response = client.delete(
        f"/activities/{activity}/participants?email={fake_email}"
    )
    assert response.status_code == 404
    error = response.json()
    assert "not found" in error["detail"].lower()


def test_unregister_from_nonexistent_activity():
    """Test unregistering from a nonexistent activity."""
    response = client.delete(
        "/activities/FakeActivity/participants?email=test@example.com"
    )
    assert response.status_code == 404


def test_root_redirect():
    """Test that root path redirects to static index."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_capacity_not_exceeded_signup():
    """Test that participant signup works when under capacity."""
    response = client.get("/activities")
    data = response.json()
    
    # Find an activity with available capacity
    for activity_name, activity_data in data.items():
        current = len(activity_data["participants"])
        max_cap = activity_data["max_participants"]
        
        if current < max_cap:
            test_email = "pytest-test@mergington.edu"
            signup_response = client.post(
                f"/activities/{activity_name}/signup?email={test_email}"
            )
            assert signup_response.status_code == 200
            break
