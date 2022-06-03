import json
import re
from flask import Blueprint, jsonify, request
from flask_login import login_user
from yaml import serialize
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


user_blueprint = Blueprint('user_api_routes', __name__, 
                            url_prefix='/api/user')

@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_user = User.query.all()
    result = [user.serialize() for user in all_user]
    response = {
        'message' : 'Returning all users',
        'result' : result
    }
    return jsonify(response)

@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = User()
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'],
                                                method='sha256')

        user.is_admin = True
        db.session.add(user)
        db.session.commit()

        response = {'message': 'User Created', 'result':user.serialize()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Error in creating response'}
    return jsonify(response)

@user_blueprint.route('login/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        response = {'message': 'username does not exist'}
        return make_response(jsonify(response), 401)
    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)
        response = {"message": 'logged in ', 'api_key':user.api_key}
        return make_response(jsonify(response), 200)