class Session():
  def __init__(self):
    self.username = None
    self.role = None

  def clear_session(self):
    self.username = None
    self.role = None

  def set_user_info(self, username, role):
    self.username = username,
    self.role = role

  def get_user_info(self):
    return {'username': self.username, 'role': self.role}
  