import os
import jwt
import datetime
from cryptography.hazmat.primitives import serialization

SECRET_KEY = "dev-secret-key"

def main(json):
    # takes in JSON data
    token = None
    if json is not None:
        temp = parse_payload(json)
        if temp is not None:
            token = temp
            return token
        else:
            print("Error generating token.")
            return None
    else:
        raise ValueError("No JSON data provided.")

def parse_payload(user_data):
    try:
        user_id = user_data['user_id']
        user_name = user_data['user_name']
        user_email = user_data['user_email']
        user_role = user_data['user_role']
        return generate_token(user_id, user_name, user_email, user_role)
    except KeyError as e:
        print(f"Missing key: {e}")

def generate_token(user_id, user_name, user_email, user_role):
    payload_data = {
        'user_id': user_id,
        'user_name': user_name,
        'user_email': user_email,
        'user_role': user_role,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }

    return jwt.encode(payload_data, SECRET_KEY, algorithm='HS256')


# for testing
if __name__ == '__main__':
    test_user = {
        'user_id': 1,
        'user_name': 'testuser',
        'user_email': 'testuser@example.com',
        'user_role': 'admin'
    }
    main(test_user)
