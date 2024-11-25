import sys
from config.settings import FontLoader, Settings
from PyQt6.QtWidgets import QApplication
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from config.session import Session

username = ''
def set_user_info(self, username, role):
    self.username = username,
    # self.role = role

def get_user_info(self):
    return {'username': self.username, 'role': self.role}

class App(QApplication):
  def __init__(self, argv):
        super().__init__(argv)
        
        # self.session = Session()
        self.init_app()
      
  def init_app(self):
      # Load fonts
      FontLoader.load_fonts()
      

if __name__ == '__main__':
    app = App(sys.argv)
    
    with open('./src/styles/global.css', 'r') as file:
      app.setStyleSheet(file.read())

    window = HomePage()
    window.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    window.show()
    sys.exit(app.exec())