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

    def test_diary_entry_creation(self):
        """
        Test a diary entry creation 
        """
        result = self.app.post("/api/v1/entries/", data=self.entry_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

    def test_create_entry_without_owner(self):
        """
        Test the creation of a diary entry through the API via 
        POST without owner field
        """
        result = self.app.post('/api/v1/user/entries/', 
                    data={       
                    "owner": "",
                    "title": "A day in space"
                                        },
                    content_type="application/json")
        self.assertEqual(result.status_code, 403)

    def test_create_entry_without_title(self):
        """
        Test the creation of a diary entry through the API via 
        POST without the title 
        """
        result = self.app.post('/api/v1/user/entries/', 
             data={       
                    "owner": "erick",
                    "title": ""
                                        },content_type="application/json")
        self.assertEqual(result.status_code, 403)

    def test_get_all_entries(self):
        """Test API to get  diary entries (GET request)."""
        result = self.app.post('/api/v1/user/entries/',
                                    content_type="application/json",
                                    data=self.entry_data)
        self.assertEqual(result.status_code, 201)
        results = self.app.get('/api/v1/user/entries/', 
            content_type="application/json")
        self.assertEqual(results.status_code, 200)
        self.assertIn('A day in space', result.data.decode('utf-8'))

    def test_get_entries_by_id(self):
        """Test API to get  user entries by the id (GET request)."""
        result = self.app.post('/api/v1/user/entries/',
                                    content_type="application/json",
                                    data=self.entry_data)
        self.assertEqual(result.status_code, 201)
        result = self.app.get('/api/v1/user/entries/1/',
                                    content_type="application/json",)
        self.assertEqual(result.status_code, 200)
if __name__ == "__main__":
    unittest.main()