# app/__init__.py

import re
from datetime import datetime
from flask_api import FlaskAPI
from flask import request, jsonify, abort
from app import models
from .models import *
from app.auth import auth_token

# local import
from instance.config import app_config

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config["development"])
    app.config.from_pyfile('config.py')

    @app.route('/api/auth/register/', methods=['POST'])
    def create_user():
        """api endpoint to create a new user"""
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            admin = data.pop('admin', False)
            regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if email == "":
                response = jsonify({'error': 'email field cannot be blank'})
                response.status_code = 400
                return response

            elif not re.match(regex, email):
                response = jsonify({
                    'error':'try entering a valid email'
                })
                response.status_code = 403
                return response

            elif username == "":
                response = jsonify({'error' : 'username field cannot be blank'})
                response.status_code = 400
                return response

            elif not re.match("^[a-zA-Z0-9_]*$", username):
                response = jsonify({'error':
                                    'Username cannot contain special characters'})
                response.status_code = 403
                return response

            elif password == "":
                response = jsonify({'error':'password field has to be filled'})
                response.status_code = 400
                return response
            elif len(password) < 6:#pylint:disable=C1801
                response = jsonify({'error':
                                    'Password should be more than 6 characters'})
                response.status_code = 403
                return response
                
            userslist = {
                'username': username,
                'email': email,
                'password': password,
                }
            u = User(**userslist)
            u.save()
            response = jsonify({'message': 'welcome you now can log in'})
            #users created successfully
            response.status_code = 201
            return response

    @app.route('/api/auth/login/', methods=['POST'])
    def login():
        """login api endpoint"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if email == "":
            response = jsonify({'error': 'email field cannot be blank'})
            response.status_code = 400
            return response
        if password == "":
            response = jsonify({'error': 'password field has to be filled'})
            response.status_code = 400
            return response

        user = get_user(email=email)
        if user is None:
            response = jsonify({'error': 'User does not exit, Register'})
            response.status_code = 400
            return response

        if user.password== password:
            access_token = User.generate_token(email)
            if access_token:
                response = {
                    'message': 'Login successful',
                    'access_token': access_token
                }
                return jsonify(response), 200
            response = {'error': 'Invalid email or password'}
            return jsonify(response), 401       
        response = {'error': 'User does not exist. Proceed to register'}
        return jsonify(response), 401

    

    return app
