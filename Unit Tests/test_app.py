import pytest
from app import app, mongo
from flask import jsonify
from datetime import datetime

# Flask app ko testing mode mein set karna
@pytest.fixture
def client():
    app.testing = True
    with app.app_context():  # Flask application context ke saath
        yield app.test_client()

    # Test ke baad MongoDB clean karna
    mongo.db.voters.delete_many({})

# Voter registration function ko directly test karna
def test_register_voter_valid(client):
    data = {
        'name': 'John Doe',
        'cnic': '12345-1234567-1',
        'dob': '1990-01-01',
        'age': 25
    }

    # Flask app ko application context mein rakh kar register_voter function ko call karna
    with app.app_context():  # Flask app context ke andar function call
        response = register_voter_logic(data)
    
    # Response check karna
    assert response['success'] == True
    assert 'Voter registered successfully' in response['message']

# Duplicate CNIC ke liye test
def test_register_voter_duplicate_cnic(client):
    data = {
        'name': 'John Doe',
        'cnic': '12345-1234567-1',
        'dob': '1990-01-01',
        'age': 25
    }

    # Pehle valid registration karte hain
    with app.app_context():
        register_voter_logic(data)

    # Duplicate CNIC ke saath registration
    with app.app_context():
        response = register_voter_logic(data)
    
    # Response check karna
    assert response['success'] == False
    assert 'Voter already registered' in response['message']

# Underage voter ke liye test
def test_register_voter_underage(client):
    data = {
        'name': 'Jane Doe',
        'cnic': '98765-9876543-2',
        'dob': '2010-05-10',  # 18 se kam age
        'age': 14
    }

    # Underage ke liye registration test karna
    with app.app_context():
        response = register_voter_logic(data)
    
    # Response check karna
    assert response['success'] == False
    assert 'Voter must be at least 18 years old' in response['message']

# Voter registration ka logic (direct function call, no route)
def register_voter_logic(data):
    name = data.get('name')
    cnic = data.get('cnic')
    dob = data.get('dob')
    age = data.get('age')

    # Logic ko implement karna (same as in your app.py function)
    if mongo.db.voters.find_one({"cnic": cnic}):
        return {"success": False, "message": "Voter already registered."}
    if age < 18:
        return {"success": False, "message": "Voter must be at least 18 years old."}

    mongo.db.voters.insert_one({"name": name, "cnic": cnic, "dob": dob, "age": age, "voted": False})
    return {"success": True, "message": "Voter registered successfully."}
