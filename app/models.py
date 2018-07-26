
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

    