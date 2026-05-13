import os
import jwt
import datetime
from cryptography.hazmat.primitives import serialization

TOKEN = None

def main(json):
    global TOKEN
    # takes in JSON data
    if json is not None:
        temp = parse_payload(json)
        if temp is not None:
            TOKEN = temp
            return None
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
    my_secret = load_key()

    if my_secret is None:
        raise Exception(
            "Private key file not found or invalid.")
    else:
        return jwt.encode(
            payload=payload_data,
            key=my_secret,
            algorithm='RS256'
    )

def load_key():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, '..', '..', 'ssh', 'id_rsa')
        with open(key_path, 'r') as f:
            private_key = f.read()
        key = serialization.load_ssh_private_key(private_key.encode(), password=b'')
        return key
    except FileNotFoundError:
        print("Private key file not found.")
        return None
    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

# for testing
if __name__ == '__main__':
        test_user = {
            'user_id': 1,
            'user_name': 'testuser',
            'user_email': 'testuser@example.com',
            'user_role': 'admin'
        }
        main(test_user)
