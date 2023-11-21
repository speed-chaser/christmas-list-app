import jwt
from datetime import datetime, timedelta
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("JWT_SECRET_KEY") 

def generate_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print("Generated Token:", token)  # debugging
    return token

def verify_token(token):
    print("running verify_token")
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']

        user = User.query.get(user_id)
        print("User ID:", user_id)  # debugging

        return user
    except jwt.ExpiredSignatureError:
        print("Expired Token")  # debugging
        return None
    except jwt.InvalidTokenError:
        print("Invalid Token")  # debugging
        return None
    