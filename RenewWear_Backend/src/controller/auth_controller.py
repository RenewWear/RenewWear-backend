from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
import service.auth_service as auth_srv
from model.user_model import User
from model.config import get_db_connection

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('name')
    login_id = data.get('login_id')
    password = data.get('pw')

    if auth_srv.register_user(username, login_id, password):
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "Registration failed"}), 400

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_id = data.get('login_id')
    password = data.get('pw')

    user = auth_srv.authenticate_user(login_id, password)
    if user:
        login_user(user)
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id FROM users WHERE login_id = %s"
        cursor.execute(query, (login_id,))
        user_id = cursor.fetchone()        
        return jsonify({"user_id": user_id['user_id']}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_controller.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful", "redirect": "http://localhost:5173/login"}), 200
