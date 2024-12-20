from config.settings import Settings, FontLoader
from database.conn import DatabaseConnection
from PyQt6.QtWidgets import QWidget, QSpacerItem,   QVBoxLayout, QHBoxLayout, QSizePolicy
from components.label import Label
from components.input import Input
from components.navbar import Navbar
from config.session import get_user_info, clear_session
from components.room_card import RoomCard
from components.button import Button
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap 
import psycopg2
class TenantHomePage(QWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setObjectName('mainWindow')

    # Load Fonts
    FontLoader.load_fonts()

    self.conn = DatabaseConnection()
    self.conn.connection()

    # Initialize UI
    self.init_ui()


  def logout(self):
    clear_session()  # Clear session data
    from pages.home_page import HomePage
    self.home_page = HomePage()
    self.home_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    self.home_page.show()
    self.destroy()
    print("Logged out")

  def open_kost_pages(self):
    print("GOW")
  
  def init_ui(self):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)

    # Get user info from session
    user_info = get_user_info()

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



    # Add Text Wrapper to the main layout
    layout.addWidget(wrapper_widget)

    wrapper_image_section_widget = QWidget()
    wrapper_image_section = QVBoxLayout(wrapper_image_section_widget)
    wrapper_image_section.setContentsMargins(0, 0, 0, 0)


    # Image Wrapper for Rooms (Room Cards)
    wrapper_image_widget = QWidget()
    wrapper_image = QHBoxLayout(wrapper_image_widget)
    wrapper_image.setAlignment(Qt.AlignmentFlag.AlignLeft)
    try: 
      query = '''
        SELECT 
          dormitory.name,
          dorm_type."name" AS dormitory_type,
          dormitory.address,
          dormitory.price
        FROM public.dormitory
        INNER JOIN dorm_type ON dormitory.dorm_type_id = dorm_type.id;
      '''
      self.conn.cursor.execute(query)
      dormitories = self.conn.cursor.fetchall()
      for dormitory in dormitories:
        dorm_name, dorm_type, dorm_address, dorm_price = dormitory
        card = RoomCard(
          dorm_name=dorm_name,
          description=dorm_address,
          image_path="src/assets/image.png",
          dorm_type=dorm_type,
          dorm_price=dorm_price
        )
        wrapper_image.addWidget(card)
    except psycopg2.Error as e:
      print("Database Error: ", e)

    wrapper_image_section.addWidget(wrapper_image_widget)

    layout.addWidget(wrapper_image_section_widget)

    footer_widget = QWidget()
    footer_layout = QHBoxLayout(footer_widget)
    footer_layout.setContentsMargins(20, 0, 20, 0)

    see_all_button = Button('See All')
    see_all_button.setFixedWidth(120)
    see_all_button.clicked.connect(self.open_kost_pages)
    footer_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    footer_layout.addWidget(see_all_button)

    layout.addStretch()
    layout.addWidget(content_widget)
    layout.addWidget(footer_widget)
    layout.addStretch()


    self.setLayout(layout)

