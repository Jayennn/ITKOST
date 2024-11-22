import bcrypt

def get_hashed_password(plain_text_password):
    """
    Hash a password for the first time using bcrypt.
    """
    
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    """
    Check a hashed password using bcrypt.
    """
    plain_text_password_bytes = plain_text_password.encode('utf-8')
    
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_text_password_bytes, hashed_password)
