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
        self.login_data = json.dumps(dict({
            "email": "erick@gmail.com",
            "password": "password"
        }))
        self.register_data = json.dumps(dict({
            "username":"erick",
            "email":"erick@gmail.com",
            "password":"password"
            }))

    def register_user(self, username="erick", email="erick@gmail.com", password="password"):
        """register method to be called in tests"""
        user_data = {
            "username": username,
            "email": email,
            "Password": password
        }
        return self.app.post(
            '/api/auth/register',
            data=json.dumps(user_data),
            content_type="application/json")

    def login_user(self, email="erick@gmail.com", password="password"):
        """ login method"""
        data = {"email": email, "Password": password}
        return self.app.post(
            '/api/auth/login',
            data=json.dumps(data),
            content_type="application/json")
        
    def create_entry(self, owner="erick", title="a good day in space"):
        """This helper method helps register a test user."""
        diary_data = {'owner': owner, 'title': title}
        return self.app.post(
                '/api/v1/entries/',
                content_type="application/json",
                data=json.dumps(diary_data))

if __name__ == "__main__":
    unittest.main()