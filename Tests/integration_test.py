import pytest
from app import app, mongo

# Fixture to set up client and MongoDB
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            # Clear the database before each test
            mongo.db.voters.drop()
            mongo.db.admins.drop()
            mongo.db.candidates.drop()
            mongo.db.elections.drop()
            yield client

# Test case for login as voter
def test_login_voter(client):
    # Insert a test voter into the MongoDB collection
    mongo.db.voters.insert_one({
        "name": "Marwa",
        "cnic": "987654321",
        "dob": "2000-07-07",
        "age": 34,
        "voted": False,
        "voter_id": "voter123"  # Adding the missing voter_id field
    })

    # Send login request
    response = client.post('/login', json={
        "cnic": "987654321",
        "dob": "2000-07-07"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['message'] == "Login successful"
    assert json_data['data']['role'] == 'voter'

# Test case for registering a new voter
def test_register_voter(client):
    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}  # Mock admin login session
    
    # Send voter registration request
    response = client.post('/register_voter', json={
        "name": "John Doe",
        "cnic": "12345",
        "dob": "2000-01-01",
        "age": 24  # Voter is eligible since age >= 18
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['message'] == "Voter registered successfully."

# Test case for login as admin
def test_login_admin(client):
    # Insert a test admin into the MongoDB collection
    mongo.db.admins.insert_one({
        "admin_id": "admin123",
        "name": "Admin",
        "cnic": "admin_cnic",
        "dob": "1970-01-01"
    })

    # Send login request for admin
    response = client.post('/login', json={
        "cnic": "admin_cnic",
        "dob": "1970-01-01"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['message'] == "Login successful"
    assert json_data['data']['role'] == 'admin'

# Test case for unsuccessful login with invalid credentials
def test_login_invalid_credentials(client):
    # Send login request with invalid credentials
    response = client.post('/login', json={
        "cnic": "wrong_cnic",
        "dob": "1970-01-01"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is False
    assert json_data['message'] == "Invalid credentials"
