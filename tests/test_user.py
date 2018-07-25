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


class AuthTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name='testing').test_client()
        self.login_data = json.dumps(dict({
            "email": "erick@gmail.com",
            "password": "password"
        }))
        self.register_data = json.dumps(dict({
            "username":"erick",
            "email":"erick@gmail.com",
            "password":"password"
            }))

    def test_registration(self):
        """Test user registration works correcty."""
        result = self.app.post("/api/auth/register/", data = self.register_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

    def test_registration_without_username(self):
        """
        Test that empty user name  cannot register
        """
        test_data = json.dumps(dict({
            "username": "",
            "email": "erick@gmail.com",
            "password": "password"
        }))
        result = self.app.post("/api/auth/register/", data = test_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 400)

    def test_registration_without_user_password(self):
        """
        Test that empty user password  cannot register
        """
        test_data = json.dumps(dict({
            "username": "erick",
            "email": "erick@gmail.com",
            "password": ""
        }))
        result = self.app.post("/api/auth/register/", data=test_data,
                                    content_type="application/json")

        self.assertEqual(result.status_code, 400)

    def test_registration_without_an_email(self):
        """
        Test that empty user email cannot register
        """
        test_data = json.dumps(dict({
            "username": "erick",
            "email": "",
            "password": "password"
        }))
        result = self.app.post("/api/auth/register/", data=test_data,
                                    content_type="application/json")

        self.assertEqual(result.status_code, 400)

    def test_registration_with_special_characters(self):
        """test that user name cannot contain special characters eg @#
        """
        test_data = json.dumps(dict({
            "username":"@erick",
            "email": "erick@email.com",
            "password":"password"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

if __name__ == "__main__":
    unittest.main()