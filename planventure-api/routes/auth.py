from functools import wraps

from database import db
from flask import Blueprint, g, jsonify, request
from models.user import User

auth_bp = Blueprint('auth', __name__)

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ')[1]
        user = User.verify_token(token)
        if not user:
            return jsonify({'message': 'Invalid or expired token'}), 401
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    if not User.validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        is_active=False
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    verification_token = user.generate_verification_token()
    # TODO: Send verification email with token
    
    return jsonify({
        'message': 'Registration successful. Please check your email to verify your account.',
        'user_id': user.id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    token = user.generate_token()
    
    # Here you would typically create a JWT token or session
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email
        }
    }), 200
