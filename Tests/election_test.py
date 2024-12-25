import pytest
from app import app, mongo
from datetime import datetime

# Set up Flask app in testing mode
@pytest.fixture
def client():
    app.testing = True
    with app.app_context():  # Flask application context
        yield app.test_client()

    # After test cleanup, remove election events data
    mongo.db.elections.delete_many({})

# Test Case: Create a new election event
def test_create_election_event(client):
    data = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    # Directly calling the create_election_event logic
    with app.app_context():
        response = create_election_event_logic(data)

    # Response validation
    assert response['success'] == True
    assert 'Election event created successfully' in response['message']

# Test Case: Edit an existing election event
def test_edit_election_event(client):
    data = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    # First, create the election event
    with app.app_context():
        create_election_event_logic(data)

    # Now, edit the election event's details
    updated_data = {
        'title': 'Presidential Election 2024 - Update',
        'date': '2024-05-22T09:00:00',
        'location': 'International Convention Center'
    }

    with app.app_context():
        response = edit_election_event_logic('Presidential Election 2024', updated_data)

    # Response validation
    assert response['success'] == True
    assert 'Election event updated successfully' in response['message']

# Test Case: Delete an election event
def test_delete_election_event(client):
    data = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    # First, create the election event
    with app.app_context():
        create_election_event_logic(data)

    # Now, delete the election event
    with app.app_context():
        response = delete_election_event_logic('Presidential Election 2024')

    # Response validation
    assert response['success'] == True
    assert 'Election event deleted successfully' in response['message']

# Test Case: Handle scheduling conflict
def test_election_event_scheduling_conflict(client):
    data1 = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    data2 = {
        'title': 'General Election 2024',
        'date': '2024-05-20T09:00:00',  # Same date and time as data1
        'location': 'International Convention Center'
    }

    # First, create the first election event
    with app.app_context():
        create_election_event_logic(data1)

    # Now, try to create a conflicting election event (same date and time)
    with app.app_context():
        response = create_election_event_logic(data2)

    # Check that it detects the scheduling conflict
    assert response['success'] == False
    assert 'Scheduling conflict detected' in response['message']

# Logic for creating an election event (to be tested)
def create_election_event_logic(data):
    title = data.get('title')
    date = datetime.fromisoformat(data.get('date'))
    location = data.get('location')

    # Check if there's already an event scheduled at the same time
    if mongo.db.elections.find_one({"date": date}):
        return {"success": False, "message": "Scheduling conflict detected."}

    # Insert the event into the database
    mongo.db.elections.insert_one({"title": title, "date": date, "location": location})
    return {"success": True, "message": "Election event created successfully."}

# Logic for editing an election event (to be tested)
def edit_election_event_logic(original_title, updated_data):
    original_event = mongo.db.elections.find_one({"title": original_title})
    if not original_event:
        return {"success": False, "message": "Event not found."}

    updated_date = datetime.fromisoformat(updated_data.get('date'))

    # Check if there's a scheduling conflict with the updated date
    if mongo.db.elections.find_one({"date": updated_date}):
        return {"success": False, "message": "Scheduling conflict detected."}

    mongo.db.elections.update_one({"title": original_title}, {"$set": updated_data})
    return {"success": True, "message": "Election event updated successfully."}

# Logic for deleting an election event (to be tested)
def delete_election_event_logic(title):
    event = mongo.db.elections.find_one({"title": title})
    if not event:
        return {"success": False, "message": "Event not found."}

    mongo.db.elections.delete_one({"title": title})
    return {"success": True, "message": "Election event deleted successfully."}
