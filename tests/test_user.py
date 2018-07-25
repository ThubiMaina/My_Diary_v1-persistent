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

    def test_registration_with_invalid_email(self):
        """test that the email supplied by the user is valid
        """
        test_data = json.dumps(dict({
            "username":"erick",
            "email": "erick@emailcom",
            "password":"password"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

    def test_registration_with_a_short_password(self):
        """test that the email supplied by the user is valid
        """
        test_data = json.dumps(dict({
            "username":"erick",
            "email": "erick@emailcom",
            "password":"pass"
            }))
        result = self.app.post("/api/auth/register/" ,data = test_data,
                            content_type = "application/json")
        self.assertEqual(result.status_code, 403)

    def test_register_with_invalid_url(self):
        """
        Test registration with an invalid url
        """
        result = self.app.post('/api/auth/regist/', data=self.register_data)
        self.assertEqual(result.status_code, 404)

    def test_already_registered_user(self):
        """
        Test that one cannot register twice
        """
        result = self.app.post("/api/auth/register/", data=self.register_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

        # Test double registration
        second_result = self.app.post("/api/auth/register/",
                                           data=self.register_data,
                                           content_type="application/json")
        self.assertEqual(second_result.status_code, 409)

    def test_login(self):
        """
        Test that a user can login successfully
        """
        result = self.app.post("/api/auth/register/", data=self.register_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

        login_res = self.app.post("/api/auth/login/", data=self.login_data,
                                          content_type="application/json")
        results = json.loads(login_res.data.decode())

        # Confirm the success message
        self.assertEqual(results["message"], "You logged in successfully.")
        # Confirm the status code and access token
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(results["access_token"])

    def test_login_incorrect_password(self):
        """Test registered user can login with an incorrect password."""
        result = self.app.post("/api/auth/register/", data=self.register_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)
        login_res = self.app.post("/api/auth/login/",
            data={"email":'erick@gmail.com',
                'password':'password1234'},
                                          content_type="application/json")
        results = json.loads(login_res.data.decode())
        self.assertEqual(result['error'], "Invalid email or password")
        self.assertEqual(login_res.status_code, 401)

    def test_login_blank_email(self):
        """Test registered user can login with a blank email."""
        result = self.app.post("/api/auth/register/", data=self.register_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)
        login_res = self.app.post("/api/auth/login/",
            data={"email":'',
                'password':'password'},
                                          content_type="application/json")
        results = json.loads(login_res.data.decode())
        self.assertEqual(result['error'], "email field cannot be blank")
        self.assertEqual(login_res.status_code, 400)

if __name__ == "__main__":
    unittest.main()