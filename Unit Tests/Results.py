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
    mongo.db.elections.delete_many({})
    mongo.db.users.delete_many({})

# Test Case: Verify vote counts, winner declaration, and report generation
def test_vote_results(client):
    voter_data = {
        'user_id': 'voter123',
        'username': 'john_doe',
        'password': 'password123',
        'email': 'john.doe@example.com'
    }

    candidate_1 = {
        'candidate_id': 'candidate001',
        'name': 'Candidate A',
        'party': 'Party X'
    }

    candidate_2 = {
        'candidate_id': 'candidate002',
        'name': 'Candidate B',
        'party': 'Party Y'
    }

    election_data = {
        'title': 'Presidential Election 2024',
        'date': '2024-05-20T09:00:00',
        'location': 'National Arena'
    }

    vote_data_1 = {
        'election_title': 'Presidential Election 2024',
        'voter_id': 'voter123',
        'candidate_id': 'candidate001'
    }

    vote_data_2 = {
        'election_title': 'Presidential Election 2024',
        'voter_id': 'voter124',
        'candidate_id': 'candidate002'
    }

    # Register voter, create election event, and add candidates
    with app.app_context():
        create_user_logic(voter_data)
        create_user_logic({
            'user_id': 'voter124',
            'username': 'jane_doe',
            'password': 'password456',
            'email': 'jane.doe@example.com'
        })
        create_election_event_logic(election_data)
        add_candidate_logic(candidate_1)
        add_candidate_logic(candidate_2)

    # Cast votes
    with app.app_context():
        cast_vote_logic(vote_data_1)
        cast_vote_logic(vote_data_2)

    # Generate results
    with app.app_context():
        results = generate_election_results('Presidential Election 2024')

    # Verify vote counts
    assert results['success'] == True
    assert results['data']['Presidential Election 2024']['vote_counts']['candidate001'] == 1
    assert results['data']['Presidential Election 2024']['vote_counts']['candidate002'] == 1

    # Verify winner declaration
    assert results['data']['Presidential Election 2024']['winner'] in ['Candidate A', 'Candidate B']

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

# Logic for adding candidates (to be tested)
def add_candidate_logic(candidate_data):
    mongo.db.candidates.insert_one(candidate_data)
    return {"success": True, "message": "Candidate added successfully."}

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

# Logic for generating election results (to be tested)
def generate_election_results(election_title):
    election = mongo.db.elections.find_one({"title": election_title})
    if not election:
        return {"success": False, "message": "Election not found"}

    votes = mongo.db.votes.find({"election_title": election_title})
    vote_counts = {}
    for vote in votes:
        candidate_id = vote['candidate_id']
        if candidate_id not in vote_counts:
            vote_counts[candidate_id] = 0
        vote_counts[candidate_id] += 1

    # Declare winner based on the highest vote count
    winner = max(vote_counts, key=vote_counts.get)
    winner_data = mongo.db.candidates.find_one({"candidate_id": winner})

    return {
        "success": True,
        "data": {
            election_title: {
                "vote_counts": vote_counts,
                "winner": winner_data['name'] if winner_data else "Unknown"
            }
        }
    }
