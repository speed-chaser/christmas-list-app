from flask import jsonify, request
from models import User, List, Item
from app import app, db
import s3_config
import boto3
from urllib.parse import urlparse
from auth_utils import generate_token, verify_token


def token_required(func):
    print("Token_required running")
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user = verify_token(token) 
        if not user:
            return jsonify({'message': 'Invalid token'}), 401
        
        # Pass the user to the wrapped function
        return func(user, *args, **kwargs)
    
    return wrapper

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    # Create the new user
    new_user = User(username=data['username'], email=data['email'])
    new_user.password = data['password']
    db.session.add(new_user)

    # Create a default list for the user
    default_list_name = f"{data['username']}'s Christmas List"
    default_list = List(name=default_list_name, user=new_user)
    db.session.add(default_list)

    db.session.commit()

    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['GET'], endpoint='get_users')
@token_required
def get_users():
    token = request.headers.get('Authorization')
    print("Received Token:", token)  # Debugging

    user = verify_token(token)
    if not user:
        print("Invalid Token")  # Debugging
        return jsonify({'message': 'Invalid token'}), 401
    
    print("User ID:", user.id)  # Debugging
    users = User.query.all()
    users_data = []
    for user in users:

        user_info = {
            'username': user.username,
            'id': user.id,
            'email': user.email,
            'lists': [{'name': list.name, 'id': list.id, 'featured': list.featured} for list in user.lists]
        }

        users_data.append(user_info)
        
    return jsonify(users_data)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data['password']


    user = User.query.filter_by(email=username_or_email).first()
    if not user:
        user = User.query.filter_by(username=username_or_email).first()

    if user and user.verify_password(password):
        token = generate_token(user)
        print("Generated Token:", token) # Debug
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid Credentials'}), 401

@app.route('/users/<user_id>/lists/<list_id>/item', methods=['POST'], endpoint='upload_item')
@token_required
def upload_item(user_id, list_id):
    data = request.json

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    list = List.query.get(list_id)
    if not list:
        return jsonify({'message': 'List not found'}), 404
    
    # Create a new item
    new_item = Item(name=data['name'], description=data['description'], list=list)

    # Upload the item's image to S3
    bucket_name = 'christmas-list-app'
    object_key = 'list-items/image.jpg'

    # Generate a pre-signed URL for the file
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key})

    parsed_url = urlparse(url)
    file_path = parsed_url.path
    print("File Path:", file_path)

    # Return the URL to the client
    return jsonify({'message': 'Item uploaded successfully', 'image_url': url}), 201

if __name__ == "__main__":
    app.run(debug=True)