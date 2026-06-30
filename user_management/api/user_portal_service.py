import configparser

from user_management.authentication.token_generation import main as generate_token
import jwt
from sqlalchemy import create_engine, text
import bcrypt
import os
import secrets
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(__file__), '..', 'db.env')
load_dotenv(_env_path)
_PROPERTIES_PATH = os.path.join(os.path.dirname(__file__), '..', 'user.properties')
_SECTION = 'tokens'

def get_stored_token(user_name: str) -> str | None:
    config = configparser.RawConfigParser()
    config.read(_PROPERTIES_PATH)
    return config.get(_SECTION, user_name, fallback=None)


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

                user_id = user_details['user_id']
                log_audit_action(user_id, user_id, 'USER_LOGIN')

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

        if verify_password(user_password, password_hash):
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

def hash_password(password):
    if not password:
        return None

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, password_hash):
    if not plain_password or not password_hash:
        return False

    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        password_hash.encode('utf-8')
    )

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

def get_user_details(token):
    try:
        public_key = load_public_key()
        if public_key is None:
            print("Error: Public key not found")
            return None, None, None, None

        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
        return decoded_token.get('user_id'), decoded_token.get('user_role'), decoded_token.get('user_name'), decoded_token.get('user_email')
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None, None, None, None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None, None, None, None

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
    connection = create_db_connection()
    if connection is None:
        raise Exception("Database connection failed")
    try:
        result = connection.execute(
            text("SELECT user_email FROM users WHERE user_email = :email"),
            {"email": email}
        )
        if result.fetchone() is None:
            return

        token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=1)
        connection.execute(
            text("INSERT INTO password_reset_tokens (token, user_email, expires_at) VALUES (:token, :email, :expires_at)"),
            {"token": token, "email": email, "expires_at": expires_at}
        )
        connection.commit()
        send_reset_email(email, token)
    finally:
        connection.close()


def confirm_password_reset(token, new_password):
    connection = create_db_connection()
    if connection is None:
        raise Exception("Database connection failed")
    try:
        result = connection.execute(
            text("""
                 SELECT p.user_email, p.expires_at, p.used, u.user_id
                 FROM password_reset_tokens p
                          JOIN users u ON p.user_email = u.user_email
                 WHERE p.token = :token
                 """),
            {"token": token}
        )
        row = result.fetchone()
        if row is None:
            raise ValueError("Invalid or expired reset token")

        user_email, expires_at, used, target_user_id = row

        if used:
            raise ValueError("Reset token has already been used")
        if datetime.now() > expires_at:
            raise ValueError("Reset token has expired")

        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        connection.execute(
            text("UPDATE users SET password_hash = :hash WHERE user_email = :email"),
            {"hash": new_hash, "email": user_email}
        )
        connection.execute(
            text("UPDATE password_reset_tokens SET used = TRUE WHERE token = :token"),
            {"token": token}
        )

        connection.commit()
        log_audit_action(target_user_id, target_user_id, 'PASSWORD_RESET')

    finally:
        connection.close()


def send_reset_email(to_email, token):
    sender = os.environ.get("GMAIL_SENDER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender or not app_password:
        raise EnvironmentError("GMAIL_SENDER and GMAIL_APP_PASSWORD must be set in db.env")

    reset_link = f"http://localhost:4200/reset-password?token={token}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender
    message["To"] = to_email
    body = f"Click the link below to reset your password (expires in 1 hour):\n\n{reset_link}"
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, app_password)
        server.sendmail(sender, to_email, message.as_string())

def get_all_users():
    connection = create_db_connection()
    if connection is None:
        return []
    try:
        result = connection.execute(
            text("SELECT user_id, user_name, user_email, user_role FROM users")
        )
        rows = result.fetchall()
        return [
            {"user_id": r[0], "user_name": r[1], "user_email": r[2], "user_role": r[3]}
            for r in rows
        ]
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        connection.close()

def delete_user(user_id):
    connection = create_db_connection()
    if connection is None:
        return False
    try:
        connection.execute(
            text("DELETE FROM users WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        connection.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        connection.close()

def update_user_role(user_id, role):
    connection = create_db_connection()
    if connection is None:
        return False
    try:
        connection.execute(
            text("UPDATE users SET user_role = :role WHERE user_id = :user_id"),
            {"role": role, "user_id": user_id}
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating user role: {e}")
        return False
    finally:
        connection.close()


def create_user(user_name, user_email, role, password):
    connection = create_db_connection()

    if connection is None:
        return False

    try:
        hashed_password = hash_password(password)

        result = connection.execute(
            text(
                "INSERT INTO users (user_name, user_email, password_hash, user_role) "
                "VALUES (:user_name, :user_email, :password_hash, :user_role) "
                "RETURNING user_id"
            ),
            {
                "user_name": user_name,
                "user_email": user_email,
                "password_hash": hashed_password,
                "user_role": role
            }
        )

        new_user_id = result.fetchone()[0]

        connection.commit()

        log_audit_action(new_user_id, new_user_id, 'USER_CREATED')

        return True

    except Exception as e:
        print(f"Error creating user: {e}")
        return False

    finally:
        connection.close()


def log_audit_action(actor_user_id: int, target_user_id: int, action_type: str):
    connection = create_db_connection()
    if connection is None:
        print("Failed to connect to DB for audit logging")
        return False

    try:
        connection.execute(
            text("""
                 INSERT INTO user_audit_logs (actor_user_id, target_user_id, action_type)
                 VALUES (:actor_id, :target_id, :action)
                 """),
            {
                "actor_id": actor_user_id,
                "target_id": target_user_id,
                "action": action_type
            }
        )
        connection.commit()
        return True
    except Exception as e:
        print(f"Error creating audit log: {e}")
        return False
    finally:
        connection.close()
    
