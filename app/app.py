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

    @app.route('/api/v1/entries/', methods=['POST'])
    @auth_token
    def create_diary_entry(current_user_email):
        """api endpoint to create a new diary entry"""
        data = request.get_json()
        owner = current_user_email
        title = data.get('title')
        content = data.get('content')
        if content == "":
            response = jsonify({'error': 'add content'})
            response.status_code = 400
            return response

        if title == "":
            response = jsonify({'error': 'provide the title for the entry'})
            response.status_code = 400
            return response
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
        one_entry = []
        entries = fetch_entries(current_user_email)
        user_entries = entries[0]
        print(user_entries)

        if not user_entries:
            abort(400)

        if user_entries[0] == entry_id:
            one_entry.append({
               'entry_id':user_entries[0],
               'title':user_entries[1],
               'content':user_entries[2],
               'owner':user_entries[3]

                })
            return jsonify(one_entry), 200
        else:
            abort(404, {"message": "not found"})


            

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['PUT'])
    @auth_token
    def update_diary_entry(entry_id, current_user_email):
        """api endpoint to edit a diary entry"""
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        entry = fetch_entries(current_user_email)
        user_entries = entry[0]
        print(user_entries)
        
        if len(user_entries)==0:
            abort(400)

        if user_entries[0] == entry_id:
            for entry in user_entries:
                update_entry(entry_id, title, content)

            return jsonify({}), 201

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['DELETE'])
    @auth_token
    def delete_entry(entry_id, current_user_email):
        """api endpoint to delete a single entry"""
        entry = fetch_entries(current_user_email)
        if not entry:
            abort(400)

        if entry[0][0] == entry_id:
            delete_entry(entry_id)

        return jsonify({'result': 'item deleted'}), 202

    return app

