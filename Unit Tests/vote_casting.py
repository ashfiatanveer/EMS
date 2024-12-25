import pytest
from app import app, mongo
from datetime import datetime

# Set up Flask app in testing mode
@pytest.fixture
def client():
    app.testing = True
    with app.app_context():  # Flask application context
        yield app.test_client()

    # After test cleanup, remove vote casting data
    mongo.db.votes.delete_many({})
    mongo.db.users.delete_many({})

# Test Case: Verify that a voter can only cast one vote per election
def test_vote_casting(client):
    voter_data = {
        'user_id': 'voter123',
        'username': 'john_doe',
        'password': 'password123',
        'email': 'john.doe@example.com'
    }

    election_data = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    vote_data = {
        'election_title': 'Presidential Election 2024',
        'voter_id': 'voter123',
        'candidate_id': 'candidate001'
    }

    # Register voter and create election event
    with app.app_context():
        create_user_logic(voter_data)
        create_election_event_logic(election_data)

    # First vote attempt
    with app.app_context():
        response = cast_vote_logic(vote_data)

    # First vote should be successful
    assert response['success'] == True
    assert 'Vote casted successfully' in response['message']

    # Second vote attempt from the same voter should fail
    with app.app_context():
        response = cast_vote_logic(vote_data)

    # The second vote should fail due to duplicate vote
    assert response['success'] == False
    assert 'You have already voted for this election' in response['message']



# Test Case: Invalid vote casting due to incorrect credentials (nonexistent election)
def test_invalid_vote_casting_incorrect_credentials(client):
    invalid_vote_data = {
        'election_title': 'Nonexistent Election 2024',
        'voter_id': 'voter123',
        'candidate_id': 'candidate001'
    }

    # Try casting vote in a non-existent election
    with app.app_context():
        response = cast_vote_logic(invalid_vote_data)

    # Response should indicate election not found
    assert response['success'] == False
    assert 'Election not found' in response['message']

# Logic for creating a user (to be tested)
def create_user_logic(user_data):
    # Check if the user already exists
    existing_user = mongo.db.users.find_one({"user_id": user_data.get('user_id')})
    if existing_user:
        return {"success": False, "message": "User already exists."}

    # Insert the new user into the database
    mongo.db.users.insert_one(user_data)
    return {"success": True, "message": "User registered successfully."}

# Logic for creating an election event (to be tested)
def create_election_event_logic(election_data):
    title = election_data.get('title')
    date = datetime.fromisoformat(election_data.get('date'))
    location = election_data.get('location')

    # Insert the election event into the database
    mongo.db.elections.insert_one({"title": title, "date": date, "location": location})
    return {"success": True, "message": "Election event created successfully."}

# Logic for casting a vote (to be tested)
def cast_vote_logic(vote_data):
    election_title = vote_data.get('election_title')
    voter_id = vote_data.get('voter_id')
    candidate_id = vote_data.get('candidate_id')

    # Check if the election exists
    election = mongo.db.elections.find_one({"title": election_title})
    if not election:
        return {"success": False, "message": "Election not found"}

    # Check if the voter has already cast their vote for this election
    existing_vote = mongo.db.votes.find_one({"election_title": election_title, "voter_id": voter_id})
    if existing_vote:
        return {"success": False, "message": "You have already voted for this election."}

    # Store the vote in the database
    mongo.db.votes.insert_one({"election_title": election_title, "voter_id": voter_id, "candidate_id": candidate_id})
    return {"success": True, "message": "Vote casted successfully."}
