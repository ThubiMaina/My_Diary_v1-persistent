
import jwt
from datetime import datetime, timedelta
import psycopg2
from db.config import config


class User:
    """user fields"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def generate_token(email):
        try:
            payload = {
            'iss': "mydiary",
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'sub': email
            }
            jwt_string = jwt.encode(payload,
             'secret', algorithm='HS256')
            return jwt_string.decode("utf-8")
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            payload = jwt.decode(token, 'secret')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return {"error": "Expired token. Please login to get a new token"}
        except jwt.InvalidTokenError:
            return {"error":"Invalid token. Please register or login"}

    