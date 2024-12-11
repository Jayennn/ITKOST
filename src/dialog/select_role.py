from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QSize
from components.button import Button
from config.settings import Settings
from config.settings import FontLoader
from config.session import set_user_info

class SelectRole(QWidget):
  def __init__(self, home_page_instance=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setObjectName('mainWindow') 

    # Get global session
    # self.session = QApplication.instance().sesi

    # Reference to the current home page
    self.home_page_instance = home_page_instance
    
    # Load Fonts
    FontLoader.load_fonts()

    # Initialize UI
    self.init_ui()

  def open_login_page(self, role):
    from pages.login_page import LoginPage

    if self.home_page_instance is not None:
        self.home_page_instance.close()

    set_user_info(username=None, role=role)

    # Open the login page
    self.login_page = LoginPage()
    self.login_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    self.login_page.show()

  
    self.close()


  def init_ui(self):
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 0, 30, 0)
    layout.setSpacing(0)
      
    role_container = QFrame()
    role_container.setStyleSheet("""
          QFrame {
              background-color: #F9F9F9;
              border: 1px solid #dcdcdc;
              border-radius: 10px;
              padding: 20px;
          }
      """)
    
    role_layout = QVBoxLayout(role_container)
    role_layout.setSpacing(20)

    # User Button
    self.user_button = Button(text='Pencari Kost', name='roles__button')
    # self.user_button.setStyleSheet("""
    #   #roles__button {
    #     font-size: 12px;
    #     font-weight: bold;
    #   }
    
    # """)
    self.user_button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.user_button.setMinimumHeight(50)
    self.user_button.clicked.connect(lambda: self.open_login_page(role='tenant'))

    # Owner Button
    self.owner_button = Button(text='Pemilik Kost', name='roles__button')
    # self.owner_button.setStyleSheet("""
    #   #roles__button {
    #     font-size: 12px;
    #     font-weight: bold;
    #   }
    
    # """)
    self.owner_button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.owner_button.setMinimumHeight(50)
    self.owner_button.clicked.connect(lambda: self.open_login_page(role='owner'))

    role_layout.addWidget(self.user_button)
    role_layout.addWidget(self.owner_button)

    # Layout
    layout.addStretch()
    layout.addWidget(role_container)
    layout.addStretch()

    self.setLayout(layout)
