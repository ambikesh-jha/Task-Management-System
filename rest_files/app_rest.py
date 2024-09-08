from flask import Flask, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from database import insert_user, find_user_by_username
from validate import validate_username, validate_password
from datetime import timedelta
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'hello_world'
app.permanent_session_lifetime = timedelta(minutes=60)
jwt = JWTManager(app)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    valid_username = validate_username(username)
    valid_password = validate_password(password)

    if valid_password and valid_username:
        success = insert_user(username, password, role)
        if success:
            return jsonify({'message': 'Signup successful'}), 201
        else:
            return jsonify({'error': 'Signup failed'}), 400
    else:
        return jsonify({'error': 'Invalid username or password'}), 400


@app.route('/login', methods=['POST'])
def login():
    # Check if the user is already logged in
    if 'username' in session:
        return jsonify({'message': f'You are already logged in as {session["username"]}'}), 200

    session.permanent = True
    data = request.json

    username = data.get('username')
    password = data.get('password')
    role = data.get('role').lower()

    user = find_user_by_username(username, role)

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['role'] = role

        # Convert ObjectId to string
        user_id_str = str(user['_id'])

        access_token = create_access_token(identity=user_id_str)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token
        }), 200
    else:
        return jsonify({'error': 'Invalid username, password, or role'}), 401



@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        session.clear()  # Clear the session
        return jsonify({'message': f'Logout successful for {username}'}), 200
    else:
        return jsonify({'error': 'No user is logged in'}), 401



# @app.route('/trainer_dashboard', methods=['GET'])
# def trainer_dashboard():
#     # Dummy implementation for testing
#     return jsonify({'message': 'Welcome to the trainer dashboard'}), 200


# @app.route('/student_dashboard', methods=['GET'])
# def student_dashboard():
#     # Dummy implementation for testing
#     return jsonify({'message': 'Welcome to the student dashboard'}), 200


if __name__ == '__main__':
    app.run(debug=True)
