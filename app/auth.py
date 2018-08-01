from functools import wraps
from flask import jsonify, make_response, request

import jwt

from app.models import User

def auth_token(func):
        """function that wraps a wrapper function"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check for the authentication token
            try:
                token = request.headers.get("Authorization")
                if not token:
                    # If there's no token provided
                    response = {
                        "error": "login required"
                    }
                    return make_response(jsonify(response)), 401

                else:
                    # Attempt to decode the token and get the user id
                    token_data = User.decode_token(token)
                    
                    if isinstance(token_data, str):
                        return func(current_user_email=token_data, *args, **kwargs)
                        
                    else:
                        return make_response(jsonify(token_data)), 401
            except jwt.InvalidTokenError:
                response = {'tokenerror':'the token has expired or has no bearer'}
                return make_response(jsonify(response)), 401

        return wrapper
