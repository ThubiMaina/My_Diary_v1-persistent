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

    
if __name__ == "__main__":
    unittest.main()