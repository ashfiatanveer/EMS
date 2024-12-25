import pytest
from app import app, mongo
from flask import jsonify


@pytest.fixture
def client():
    app.testing = True
    with app.app_context():  
        yield app.test_client()  

   
    mongo.db.candidates.delete_many({})

def test_add_candidate_valid(client):
    data = {
        'name': 'John Doe',
        'party': 'Democratic Party'
    }

    # Directly calling the add_candidate function logic
    with app.app_context():
        response = add_candidate_logic(data)

    # Response validation
    assert response['success'] == True
    assert 'Candidate added successfully' in response['message']

# Test Case: Handle duplicate candidate
def test_add_candidate_duplicate(client):
    data = {
        'name': 'John Doe',
        'party': 'Democratic Party'
    }

    # First, add the candidate
    with app.app_context():
        add_candidate_logic(data)

    # Try to add the same candidate again (duplicate)
    with app.app_context():
        response = add_candidate_logic(data)

    # Check that it catches the duplicate candidate
    assert response['success'] == False
    assert 'Candidate already exists' in response['message']

# Logic for adding a candidate (to be tested)
def add_candidate_logic(data):
    name = data.get('name')
    party = data.get('party')

    # Check if the candidate already exists in the database
    if mongo.db.candidates.find_one({"name": name, "party": party}):
        return {"success": False, "message": "Candidate already exists."}

    # Insert the candidate into the database
    mongo.db.candidates.insert_one({"name": name, "party": party})
    return {"success": True, "message": "Candidate added successfully."}
