from user_management.authentication.token_generation import main as generate_token
import jwt
from sqlalchemy import create_engine, text
import bcrypt
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from supabase import create_client, Client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def validate_login(json):
    try:
        user_name = json['user_name']
        user_password = json['password']
        if validate_credentials(user_name, user_password):
            user_details = get_user_info(user_name)
            if user_details is None:

                return False
            try:
                token = generate_token(user_details)
                return token
            except Exception as e:
                print(f"Error generating token: {e}")
                return False
        else:
            return False
    except KeyError:
        return False

def validate_credentials(user_name, user_password):
    connection = create_db_connection()
    if connection is None:
        return False

    try:
        print(f"Validating credentials for user: {user_name}")
        result = connection.execute(
            text("SELECT password_hash FROM users WHERE user_name = :user_name"),
            {"user_name": user_name}
        )
        user_row = result.fetchone()

        if user_row is None:
            print(f"User {user_name} not found in database")
            return False

        password_hash = user_row[0]

        # compare provided password with stored hash using bcrypt
        if bcrypt.checkpw(user_password.encode('utf-8'), password_hash.encode('utf-8')):
            print(f"Password validated successfully for user: {user_name}")
            return True
        else:
            print(f"Invalid password for user: {user_name}")
            return False

    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False
    finally:
        if connection:
            connection.close()

def get_user_info(user_name):
    connection = create_db_connection()
    if connection is None:
        return None

    try:
        result = connection.execute(
            text("SELECT user_id, user_name, user_email, user_role FROM users WHERE user_name = :user_name"),
            {"user_name": user_name}
        )
        user_row = result.fetchone()

        if user_row is None:
            print(f"User {user_name} not found in database")
            return None

        return {
            "user_id": user_row[0],
            "user_name": user_row[1],
            "user_email": user_row[2],
            "user_role": user_row[3]
        }
    except Exception as e:
        print(f"Error retrieving user info: {e}")
        return None
    finally:
        if connection:
            connection.close()

def verify_token(token):
    try:
        public_key = load_public_key()
        if public_key is None:
            print("Error: Public key not found")
            return False

        jwt.decode(token, public_key, algorithms=['RS256'])
        return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return False
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return False
    except Exception as e:
        print(f"Error verifying token: {e}")
        return False

def get_user_id_and_role(token):
    try:
        public_key = load_public_key()
        if public_key is None:
            print("Error: Public key not found")
            return None, None

        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
        return decoded_token.get('user_id'), decoded_token.get('user_role')
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None, None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None, None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None, None

def create_db_connection():
    try:
        engine = create_engine("postgresql://admin:admin123@localhost:5432/user_management")
        connection = engine.connect()
        return connection
    except Exception as e:
        print(f"Error creating database connection: {e}")
        return None

def load_public_key():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(script_dir, '..', '..', 'ssh', 'id_rsa.pub')

        with open(key_path, 'r') as f:
            public_key = f.read()
        key = serialization.load_ssh_public_key(public_key.encode(), backend=default_backend())
        return key
    except FileNotFoundError:
        print("Public key file not found at ssh/id_rsa.pub")
        return None
    except Exception as e:
        print(f"Error loading public key: {e}")
        return None

def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(
            email,
            {
                # point this to your local frontend application
                "redirect_to": "http://localhost:3000/update-password",
            }
        )
    except Exception as e:
        print(f"Error triggering Supabase password reset: {e}")
        raise
