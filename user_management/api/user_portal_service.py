from user_management.authentication.token_generation import main as generate_token
import jwt

def validate_login(json):
    try:
        user_name = json['user_name']
        user_password = json['password']
        # Placeholder for actual validation logic
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
    # Placeholder for actual credential validation logic
    # database should be queried for user_name and user_password
    return True

def get_user_info(user_name):
    # get user info from database and return as json
    # NOTE: Must include user_id for token generation
    return {"user_id": 1, "user_name": user_name, "user_email": "", "user_role": "admin"}

def verify_token(token):
    if jwt.decode(token, verify=True):
        return True
    else:
        return False

def get_user_id_and_role(token):
    decoded_token = jwt.decode(token, verify=True)
    return decoded_token['user_id'], decoded_token['user_role']
