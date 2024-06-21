from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from email_validator import validate_email, EmailNotValidError
from hfsa_app.models.user import User
from hfsa_app import db
from flask_jwt_extended import JWTManager
from datetime import datetime, date
import logging
from functools import wraps

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')
bcrypt = Bcrypt()
jwt = JWTManager()

# Admin required decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Get all users
@user_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
            'contact_number': user.contact_number,
            'address': user.address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
        }
        output.append(user_data)
    return jsonify({'users': output})

# Get a specific user
@user_bp.route('/user/<int:id>', methods=['GET'])
@admin_required
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
        'contact_number': user.contact_number,
        'address': user.address,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
    }
    return jsonify(user_data)

# Register a user
@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        validate_email(email)

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            name=data.get('name'),
            email=email,
            password=hashed_password,
            role=data.get('role', 'user'),
            date_of_birth=datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d'),
            contact_number=data.get('contact_number'),
            address=data.get('address'),
    
        )

        db.session.add(new_user)
        db.session.commit()

        user_details = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'role': new_user.role,
            'date_of_birth': new_user.date_of_birth.strftime('%Y-%m-%d'),
            'contact_number': new_user.contact_number,
            'address': new_user.address,
            
        }

        return jsonify({'message': 'User registered successfully', 'user': user_details}), 201

    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Update a user
@user_bp.route('/user/<int:id>', methods=['PUT'])
# @jwt_required()
@admin_required
def update_user(id):
    try:
        user = User.query.get_or_404(id)
        data = request.get_json()

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        user.date_of_birth = datetime.strptime(data.get('date_of_birth', user.date_of_birth.strftime('%Y-%m-%d')), '%Y-%m-%d')
        user.contact_number = data.get('contact_number', user.contact_number)
        user.address = data.get('address', user.address)
        
        if 'password' in data and data['password']:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        db.session.commit()
        
        # Return updated user details
        user_details = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
            'contact_number': user.contact_number,
            'address': user.address,
        
        }

        return jsonify({'message': 'User updated successfully', 'user': user_details})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a user
@user_bp.route('/user/<int:id>', methods=['DELETE'])
# @jwt_required()
@admin_required
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500


# Authentication endpoint to handle user login
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # if not bcrypt.check_password_hash(user.password, password):
        #     return jsonify({'error': 'Invalid password'}), 401

        # Initialize the is_admin flag
        is_admin = False

        # Check if the user is an admin based on their credentials
        if email == 'HopeField@info.com' and password == 'Hope256':
            is_admin = True

        user_info = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,  
            'is_admin': is_admin  
        }

        access_token = create_access_token(identity=user_info)
        redirect_url = determine_redirect_url(user.role)  

        return jsonify({
            'access_token': access_token,
            'user': user_info,
            'redirect_url': redirect_url,
            'is_admin': is_admin  
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to determine redirect URL based on user role
def determine_redirect_url(role):
    if role == 'admin':
        return '/'  
    else:
        return '/admin'   