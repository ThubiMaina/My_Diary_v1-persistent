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


class UserTestCase(unittest.TestCase):
    """Test case for the user creation and login"""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app('testing').test_client()
        self.user_data = json.dumps(dict({
                    "username": "erick",
                    "email": "erick@gmail.com",
                    "password": "password"
                }))

    def register_user(self, email="erick@gmail.com", username="erick",
                      password="password"):
        """This helper method helps register a test user."""
        user_data = {'email': email, 'username': username,
                     'password': password}
        return self.app.post(
                '/api/auth/register/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data))

    def login_user(self, email="user@gmail.com", password="password"):
        """This helper method helps log in a test user."""
        user_data = {'email': email, 'password': password}
        return self.app.post(
                '/api/auth/login/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(user_data)
               )

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
        self.assertEqual(result.status_code, 401)

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

        self.assertEqual(result.status_code, 401)

    def test_registration_with_spaces_as_password(self):
        """
        Test that empty user password  cannot register
        """
        test_data = json.dumps(dict({
            "username": "erick",
            "email": "erick@gmail.com",
            "password": "       "
        }))
        result = self.app.post("/api/auth/register/", data=test_data,
                                    content_type="application/json")
        results = json.loads(result.data.decode())
        self.assertEqual(results['error'],
                         "please avoid using spaces in your password")

        self.assertEqual(result.status_code, 403)

    def test_registration_with_spaces_as_username(self):
        """
        Test that empty user password  cannot register
        """
        result = self.register_user("test@mail.com", "     ", "password")
        res = json.loads(result.data.decode())
        self.assertEqual(res['error'],"Your first value  must NOT !! be a space")
        self.assertEqual(result.status_code, 403)

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

        self.assertEqual(result.status_code, 401)

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
        """test that the password is more than five characters
        """
        result = self.register_user("test@mail.com", "test", "pass")
        res = json.loads(result.data.decode())
        self.assertEqual(res['error'],
                         "Password should be more than 6 characters")
        self.assertEqual(result.status_code, 403)

    def test_register_with_invalid_url(self):
        """
        Test registration with an invalid url
        """
        result = self.app.post('/api/auth/regist/', data=self.user_data)
        self.assertEqual(result.status_code, 404)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        self.register_user("erick@mail.com", "erick", "password")
        second_res = self.register_user("erick@mail.com",
                                        "erick", "password")
        self.assertEqual(second_res.status_code, 409)

    def test_user_login(self):
        """Test registered user can login."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("user@mail.com", "testpass")
        self.assertEqual(login_res.status_code, 200)


    def test_login_incorrect_password(self):
        """Test registered user can login with an incorrect password."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("user@mail.com", "testpas")
        self.assertEqual(login_res.status_code, 401)

    def test_login_blank_email(self):
        """Test registered user can login with a blank email."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("", "testpass")
        self.assertEqual(login_res.status_code, 401)

    def test_login_blank_password(self):
        """Test registered user can login with a blank email."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("user@mail", "")
        self.assertEqual(login_res.status_code, 401)

    def test_login_with_spaces_as_password(self):
        """Test registered user can login with a blank email."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("user@mail", "      ")
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['error'], "please avoid using spaces in your password")
        self.assertEqual(login_res.status_code, 403)

    def test_login_with_spaces_as_email(self):
        """Test registered user can login with a blank email."""
        self.register_user("user@mail.com", "testuser", "testpass")
        login_res = self.login_user("     ", "testpass")
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['error'], "email field cannot contain spaces")
        self.assertEqual(login_res.status_code, 403)

    def test_login_non_registered_user(self):
        """
        Test that non registered users cannot log in
        """
        unregistered = json.dumps(dict({
            "username": "tiaroot",
            "email": "tiaroot@email.com",
            "password": "invalidpassword"
        }))

        result = self.app.post("/api/auth/login/", data=unregistered,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 409)

    def test_login_with_a_nonexistent_url(self):
        """
        Test login with invalid url
        """
        response = self.app.post('/api/auth/logon/', data=self.user_data)
        self.assertEqual(response.status_code, 404)
if __name__ == "__main__":
    unittest.main()