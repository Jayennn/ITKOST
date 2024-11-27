from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QSize
from components.button import Button
from config.settings import Settings
from config.settings import FontLoader


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

    # Open the login page
    self.login_page = LoginPage()
    self.login_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    self.login_page.show()

  
    self.close()
    # print(role)
    # self.session.set_user_info('budi', 'ayam')


  def init_ui(self):
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 0, 30, 0)
    layout.setSpacing(0)

    # User Button
    self.user_button = Button(text='Pencari Kost', name='roles')
    self.user_button.setIconSize(QSize(24, 24))
    self.user_button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.user_button.setMinimumHeight(40)
    self.user_button.clicked.connect(lambda: self.open_login_page(role=1))

    # Owner Button
    self.owner_button = Button(text='Pemilik Kost', name='roles')
    self.owner_button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.owner_button.setMinimumHeight(40)
    self.owner_button.clicked.connect(lambda: self.open_login_page(role=2))

    # Layout
    layout.addStretch()
    layout.addWidget(self.user_button)
    layout.setSpacing(10)
    layout.addWidget(self.owner_button)
    layout.addStretch()

    self.setLayout(layout)
