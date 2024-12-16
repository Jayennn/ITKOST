# config/session.py
_session_data = {}

def set_user_info(username, role):
    global _session_data
    _session_data['username'] = username
    _session_data['role'] = role
    print("session.py: ", username, role)

def get_user_info():
    global _session_data
    return _session_data

def clear_session():
    global _session_data
    _session_data.clear()
