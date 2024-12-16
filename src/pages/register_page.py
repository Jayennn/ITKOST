from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QComboBox
import psycopg2
from config.settings import FontLoader, Settings
from database.conn import DatabaseConnection
from components.index import Label
from components.navbar import Navbar
from components.input import Input
from components.button import Button
from widgets.container import Container
from config.hashPassword import get_hashed_password
from PyQt6.QtGui import QFont

class RegisterPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow')

        # Load Fonts
        FontLoader.load_fonts()

        # Initialize UI
        self.init_ui()

        # Initialize database connection
        self.conn = DatabaseConnection()
        self.conn.connection()

    def form_submit(self):
        # Collect user input
        value = {
            'phone_number': self.phone_number.text(),
            'password': self.password.text(),
            'name': self.full_name.text(),
            'role': 'tenant' if self.role_selector.currentText() == 'Pencari Kost (Tenant)' else 'owner'
        }

        try:
            # Insert user data into the database
            query = """
            INSERT INTO public.user (name, phone_number, password, role) 
            VALUES (%s, %s, %s, %s)
            """
            self.conn.cursor.execute(
                query, 
                (value['name'], value['phone_number'], value['password'], value['role'])
            )
            self.conn.conn.commit()
            print("User registered successfully!")
            self.open_login_page()

        except psycopg2.Error as e:
            print("Database Error: ", e)

    def validate_form(self):
        is_valid = all([
            self.full_name.text().strip(),
            self.phone_number.text().strip(),
            self.password.text().strip(),
            self.password_verify.text().strip(),
            self.password.text() == self.password_verify.text()
        ])

        self.button_register.setDisabled(not is_valid)

    def open_login_page(self):
        from pages.login_page import LoginPage
        self.login_page = LoginPage()
        self.login_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.login_page.show()
        self.destroy()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Navbar
        navbar = Navbar(self)
        navbar.button.clicked.connect(self.open_login_page)
        layout.addWidget(navbar)

        # Container for content
        container = Container()

        # Heading
        heading = Label(
            'Daftar Akun',
            font_size=18,
            font_weights=Settings.FONT_WEIGHTS['black']
        )
        heading.setObjectName('heading')
        container.container_layout.addWidget(heading)

        subheading = Label(
            'Masukkan data diri kamu!',
            font_size=10,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        subheading.setObjectName('subheading')
        container.container_layout.addWidget(subheading)

        container.container_layout.addSpacing(25)

        # Input Full Name
        full_name_label = Label('Nama Lengkap')
        self.full_name = Input(placeholder='Masukkan nama lengkap sesuai identitas')
        self.full_name.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(full_name_label)
        container.container_layout.addWidget(self.full_name)

        # Input Phone Number
        phone_number_label = Label('Nomor Handphone')
        self.phone_number = Input(placeholder='Nomor Handphone')
        self.phone_number.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(phone_number_label)
        container.container_layout.addWidget(self.phone_number)

        # Input Password
        password_label = Label('Password')
        self.password = Input(placeholder='Password', password_mode=True)
        self.password.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(password_label)
        container.container_layout.addWidget(self.password)

        # Input Password Verify
        password_verify_label = Label('Konfirmasi Password')
        self.password_verify = Input(placeholder='Konfirmasi Password', password_mode=True)
        self.password_verify.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(password_verify_label)
        container.container_layout.addWidget(self.password_verify)

        # Role Selection
        role_label = Label('Pilih Peran')
        self.role_selector = QComboBox()
        self.role_selector.addItems(['Pencari Kost (Tenant)', 'Pemilik Kost (Owner)'])
        self.role_selector.setObjectName('role_selector')
        self.role_selector.setFont(QFont(Settings.FONT_FAMILY, 8))
        self.role_selector.setStyleSheet('''
          QComboBox#role_selector {
            width: 100%;
            border: 1px #E4E4E7 solid;
            background-color: #f9f9f9;
            color: #1A1A1A;
            padding: 12px 8px;
            border-radius: 6px;
            height: 14px;
          }
          QComboBox:editable {
            background-color: white;
          }
          QComboBox::drop-down {
            background-color: white;
          }
          QComboBox:!editable:on, QComboBox::drop-down:editable:on {
            background-color: white;
          }
          QComboBox QAbstractItemView {
            border: 1px solid #E4E4E7;
            background-color: white;
            color: #1A1A1A;
          } 
        ''')
        container.container_layout.addWidget(role_label)
        container.container_layout.addWidget(self.role_selector)

        container.container_layout.addSpacing(25)

        # Register Button
        self.button_register = Button('Register', 'btn_register')
        self.button_register.setDisabled(True)
        self.button_register.clicked.connect(self.form_submit)
        container.container_layout.addWidget(self.button_register)

        layout.addStretch()
        layout.addWidget(container.container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
