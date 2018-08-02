import unittest
import json
import sys
import os
import inspect

currentdir = os.path.dirname(

    os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir)

sys.path.insert(0, parentdir)


from app.app import create_app

class EntryTestCase(unittest.TestCase):
    """Test case for the Diary entries"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name='testing').test_client()
        self.entry_data = json.dumps(dict({
                    "owner": "erick",
                    "title": "A day in space"
                }))
    def register_user(self, email="erick@gmail.com", username="erick",
                      password="password"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username,
                     'password': password}
        return self.app.post(
                '/api/auth/register/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

    def login_user(self, email="erick@gmail.com", password="password"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        result =  self.app.post(
                '/api/auth/login/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def create(self, title="Visit kenya",
        content="Eat lots of nyama choma"):
        """This helper method helps register a test user."""
        self.register_user()
        access_token = self.login_user()
        diary_data = { 'title': title, 'content':content}
        result = self.app.post("/api/v1/entries/", 
                                data=diary_data,
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        return result

    def test_diary_entry(self):
        """
        Test a diary entry
        """
        self.register_user()
        access_token = self.login_user()
        self.create()
        # access_token = json.loads(result.data.decode())['access_token']
        result = self.app.post("/api/v1/entries/", 
                                data=self.entry_data,
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        res = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 201)
        self.assertEqual(res['message'], "entry created")


    def test_get_empty_entries(self):
        """Test API to get entries (GET request)."""
        self.register_user()
        access_token = self.login_user()
        result = self.app.get("/api/v1/entries/", 
                                headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        self.assertEqual(result.status_code, 404)
    

    def test_empty_post_entries(self):
        """Test bad request on post method"""
        self.register_user()
        access_token = self.login_user()
        empty = self.app.post("/api/v1/entries/", data={},
                                    headers={'Content-Type': 'application/json',
                         'Authorization': access_token})

        self.assertEqual(empty.status_code, 400)

    def test_invalid_access_token(self):
        """Test API can check for a valid access token"""
        self.register_user()
        result = self.login_user()
        access_token = "deyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlcmlja0BnbWFpbC5jb20iLCJleHAiOjE1MzI3ODkwNzAsImlzcyI6Im15ZGlhcnkiLCJpYXQiOjE1MzI3ODcyNzB9.m6kLmdUqf4XLq7TIkb97HCCSjIZLJ8kvmwaOah1BClU"
        post_data = self.app.post("/api/v1/entries/", data={'owner':'erick',
                        'title' :'go to the park'},
                          headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        result = json.loads(post_data.data.decode())
        self.assertEqual(post_data.status_code, 401)
        self.assertEqual(result['error'], "Invalid token. Please register or login")

    def test_empty_access_token(self):
        """Test API can check for an empty access token"""
        self.register_user()
        result = self.login_user()
        access_token = ""
        post_data = self.app.post("/api/v1/entries/", data={'owner':'erick',
                        'title' :'go to the park'},
                          headers={'Content-Type': 'application/json',
                         'Authorization': access_token})
        result = json.loads(post_data.data.decode())
        self.assertEqual(post_data.status_code, 401)
        self.assertEqual(result['error'], "login required")
        

    def test_entry_without_title(self):
        """Test if an entry can be created without a title"""
        entry_res = self.create( "", "content added here")
        self.assertEqual(entry_res.status_code, 400)

    def test_if_entry_exists(self):
        """Test that a user cannot create an entry twice"""
        self.create("a walk in the park", "some content")
        second_res = self.create("a walk in the park", "some content")
        self.assertEqual(second_res.status_code, 400)



if __name__ == "__main__":
    unittest.main()