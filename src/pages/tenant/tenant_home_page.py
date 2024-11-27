from config.settings import Settings, FontLoader
from database.conn import DatabaseConnection
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from components.label import Label
from components.input import Input
from components.navbar import Navbar
from config.session import get_user_info, clear_session
from components.room_card import RoomCard
class TenantHomePage(QWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setObjectName('mainWindow')

    # Load Fonts
    FontLoader.load_fonts()


    # Initialize UI
    self.init_ui()

    self.conn = DatabaseConnection()
    self.conn.connection()

  def logout(self):
    clear_session()  # Clear session data
    from pages.home_page import HomePage
    self.home_page = HomePage()
    self.home_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    self.home_page.show()
    self.destroy()
    print("Logged out")
  
  def init_ui(self):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)

    # Get user info from session
    user_info = get_user_info()
    # if not user_info or not user_info.get('username'):
    #     print("No session found, redirecting to login page.")
    #     from pages.login_page import LoginPage  # Import the LoginPage
    #     self.login_page = LoginPage()
    #     self.login_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    #     self.login_page.show()
    #     self.destroy()
    #     return

    # print("Session in TenantHomePage:", user_info)

    # Navbar
    navbar = Navbar(self)
    navbar.button.setText('Logout')
    navbar.button.clicked.connect(self.logout)
    layout.addWidget(navbar)

    # Content Section
    content_widget = QWidget()
    horizontal_layout = QHBoxLayout()
    content_widget.setLayout(horizontal_layout)

    horizontal_layout.setContentsMargins(20, 0, 20, 0)
    horizontal_layout.addSpacing(10)

    # Text Wrapper (Welcome & Persuasive Text)
    wrapper_widget = QWidget()
    wrapper_top = QVBoxLayout(wrapper_widget)
    wrapper_top.setContentsMargins(20, 0, 20, 0)

    welcome_heading = Label(
      f"Selamat datang, {user_info.get('username', 'Guest')}",
      font_size=16,
      font_weights=Settings.FONT_WEIGHTS['black']
    )
    wrapper_top.addWidget(welcome_heading)

    persuasive_text = Label(
      f"Dapatkan infonya dan langsung sewa di ITKOST",
      font_size=11,
      font_weights=Settings.FONT_WEIGHTS['medium']
    )
    wrapper_top.addWidget(persuasive_text)


    # search_bar = Input()


    # Add Text Wrapper to the main layout
    layout.addWidget(wrapper_widget)

    # Image Wrapper for Rooms (Room Cards)
    wrapper_image_widget = QWidget()
    wrapper_image = QHBoxLayout(wrapper_image_widget)
    rooms = [
        {"image": "src/assets/image.png", "title": "Room A", "description": "A cozy room with all amenities."},
        {"image": "src/assets/image.png", "title": "Room A", "description": "A cozy room with all amenities."},
        {"image": "src/assets/image.png", "title": "Room A", "description": "A cozy room with all amenities."},
        # You can add more room data here
    ]

    for room in rooms:
        card = RoomCard(room["image"], room["title"], room["description"])
        # card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        wrapper_image.addWidget(card)

    # Add Image Wrapper below Text Wrapper
    layout.addWidget(wrapper_image_widget)

    # Add Content and Stretch to Layout
    layout.addWidget(content_widget)
    layout.addStretch()

    # Set the main layout for the page
    self.setLayout(layout)

