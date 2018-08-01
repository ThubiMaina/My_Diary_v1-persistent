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

            if not re.match(regex, email):
                response = jsonify({
                    'error':'try entering a valid email'
                })
                response.status_code = 403
                return response

            if username == "":
                response = jsonify({'error' : 'username field cannot be blank'})
                response.status_code = 400
                return response

            if username:
                stripped_name = username.strip()
                if len(stripped_name) == 0:
                    response = jsonify({'error':
                    'Your first value  must NOT !! be a space'})
                    response.status_code = 403
                    return response

            if not re.match("^[a-zA-Z0-9_ ]*$", username):
                response = jsonify({'error':
                                    'Username cannot contain special characters'})
                response.status_code = 403
                return response

            if password == "":
                response = jsonify({'error':'password field has to be filled'})
                response.status_code = 400
                return response

            if password:
                stripped_pass = password.strip()
                if len(stripped_pass) == 0:
                    response = jsonify({'error':
                    'please avoid using spaces in your password'})
                    response.status_code = 403
                    return response

            if len(password) < 6:#pylint:disable=C1801
                response = jsonify({'error':
                                    'Password should be more than 6 characters'})
                response.status_code = 403
                return response

            user = get_user(email=email)
            if user is not None:
                response = jsonify({'error':'that user exists'})
                response.status_code = 409
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

        if email:
                stripped_mail = email.strip()
                if len(stripped_mail) == 0:
                    response = jsonify({'error':
                    'email field cannot contain spaces'})
                    response.status_code = 403
                    return response
        if password == "":
            response = jsonify({'error': 'password field has to be filled'})
            response.status_code = 400
            return response

        if password:
                stripped_pass = password.strip()
                if len(stripped_pass) == 0:
                    response = jsonify({'error':
                    'please avoid using spaces in your password'})
                    response.status_code = 403
                    return response

        user = get_user(email=email)
        if user is None:
            response = jsonify({'error': 'User does not exit, Register'})
            response.status_code = 409
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

    @app.errorhandler(404)
    def page_not_found(e):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def server_error(e):
        response = jsonify({'error': 'Internal server error'})
        response.status_code = 500
        return response

    @app.route('/api/v1/entries/', methods=['POST'])
    @auth_token
    def create_diary_entry(current_user_email):
        """api endpoint to create a new diary entry"""
        data = request.get_json()
        owner = current_user_email
        title = data.get('title')
        content = data.get('content')

        if title == "":
            response = jsonify({'error': 'provide the title for the entry'})
            response.status_code = 400
            return response

        if title:
                stripped_title = title.strip()
                if len(stripped_title) == 0:
                    response = jsonify({'error':
                    'title should not start with spaces'})
                    response.status_code = 403
                    return response

        if content == "":
            response = jsonify({'error': 'add content'})
            response.status_code = 400
            return response

        
        if content:
                stripped_content = content.strip()
                if len(stripped_content) == 0:
                    response = jsonify({'error':
                    'field cannot start with spaces'})
                    response.status_code = 403
                    return response
        # entries = fetch_entries(current_user_email)
        # entries_user = [entry for entry in entries if entry[3] == owner]
        # for title in entries_user:
        #     if title[1] == 'title':
        #         abort(400)
        Entry = {
            'owner': owner,
            'title': title,
            'content':content}

        diary_entry = DiaryEntries(**Entry)
        diary_entry.save_entry()
        response = jsonify({"message": "entry created"})
        response.status_code = 201
        return response

    @app.route('/api/v1/entries/', methods=['GET'])
    @auth_token
    def get_entries(current_user_email):
        """api endpoint to get a list of diary entries"""
        DiaryList = []
        entries = fetch_entries(current_user_email)

        if not entries:
            abort(400)

        for diary_entry in entries:
            DiaryList.append({'date': datetime.utcnow(),
                              'owner': diary_entry[3],
                              'entry_id': diary_entry[0],
                              'title': diary_entry[1],
                              'content':diary_entry[2]
                             })
        return jsonify(DiaryList), 200

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['GET'])
    @auth_token
    def get_single_entry(entry_id, current_user_email):
        """api endpoint to get a single diary entry"""
        entries = fetch_entries(current_user_email)

        entries_user = [entry for entry in entries if entry[0] == entry_id]

        if len(entries_user) == 0:
            abort(400)
        return jsonify({
            
            "entry":entries_user
            }),200
            

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['PUT'])
    @auth_token
    def update_diary_entry(entry_id, current_user_email):
        """api endpoint to edit a diary entry"""
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        if title == "":
            response = jsonify({'error': 'provide the title for the entry'})
            response.status_code = 400
            return response

        if title:
                stripped_title = title.strip()
                if len(stripped_title) == 0:
                    response = jsonify({'error':
                    'title should not start with spaces'})
                    response.status_code = 403
                    return response

        if content == "":
            response = jsonify({'error': 'add content'})
            response.status_code = 400
            return response

        
        if content:
                stripped_content = content.strip()
                if len(stripped_content) == 0:
                    response = jsonify({'error':
                    'field cannot start with spaces'})
                    response.status_code = 403
                    return response
        entries = fetch_entries(current_user_email)
        user_entries = [entry for entry in entries if entry[0] == entry_id]
        
        if len(user_entries)==0:
            abort(400)

        update_entry(entry_id, title, content)

        return jsonify({'message':'updated'}), 201

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['DELETE'])
    @auth_token
    def delete_entry(entry_id, current_user_email):
        """api endpoint to delete a single entry"""
        entries = fetch_entries(current_user_email)
        if not entries:
            abort(400)

        user_entries = [entry for entry in entries if entry[0] == entry_id]
        if len(user_entries) == 0:
            abort(400)
        delete_entry()

        return jsonify({'result': 'item deleted'}), 202

    return app

