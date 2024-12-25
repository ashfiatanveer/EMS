import unittest
from app import app, mongo
from flask import jsonify
from datetime import datetime

class TestRoleBasedAccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This function will be called once before running the tests
        cls.client = app.test_client()  # Create a test client for Flask app

    def setUp(self):
        # This function will run before each test
        # You can insert test data here for each test case
        mongo.db.voters.delete_many({})  # Clear the voters collection before each test
        mongo.db.admins.delete_many({})  # Clear the admins collection before each test
        mongo.db.candidates.delete_many({})  # Clear the candidates collection before each test
        mongo.db.elections.delete_many({})  # Clear the elections collection before each test

        # Insert test users into the database
        mongo.db.voters.insert_one({"voter_id": "voter1", "cnic": "voter_cnic", "dob": "1990-01-01", "age": 30, "voted": False})
        mongo.db.admins.insert_one({"admin_id": "admin", "name": "Admin", "cnic": "admin_cnic", "dob": "1970-01-01"})
        mongo.db.candidates.insert_one({"candidate_id": "candidate1", "name": "John Doe", "party": "Party A"})
        
        # Insert a dummy election for voting
        mongo.db.elections.insert_one({
            "name": "Election 2024",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
            "votes": {}
        })

    def login(self, cnic, dob):
        """Helper function to log in a user."""
        return self.client.post('/login', json={"cnic": cnic, "dob": dob})

    def test_admin_access(self):
        # Login as Admin
        response = self.login("admin_cnic", "1970-01-01")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Login successful")

        # Try accessing an admin-required route
        response = self.client.post('/create_election', json={
            "name": "Election 2024",
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat()
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Election created successfully.")

    def test_voter_access(self):
        # Login as Voter
        response = self.login("voter_cnic", "1990-01-01")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Login successful")

        # Try accessing a voter-specific route
        response = self.client.post('/cast_vote', json={
            "election_id": "election_id",
            "candidate_id": "candidate1"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Vote cast successfully.")

        # Try accessing an admin-required route
        response = self.client.post('/create_election', json={
            "name": "Election 2024",
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat()
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_candidate_access(self):
        # Login as Candidate
        response = self.login("candidate_cnic", "1980-01-01")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Login successful")

        # Try accessing a voter-specific route (should be allowed)
        response = self.client.post('/cast_vote', json={
            "election_id": "election_id",
            "candidate_id": "candidate1"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Vote cast successfully.")

        # Try accessing an admin-required route
        response = self.client.post('/create_election', json={
            "name": "Election 2024",
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat()
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login page

if __name__ == "__main__":
    unittest.main()
