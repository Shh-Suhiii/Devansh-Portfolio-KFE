from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from db.connection import mysql
from werkzeug.security import check_password_hash
from models.admin_user_model import AdminUser

auth_bp = Blueprint('auth_bp', __name__)

# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data and check_password_hash(user_data[2], password):
        user = AdminUser(id=user_data[0], email=user_data[1])
        # login_user(user)  # Disabled for API testing
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Logout Route
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200