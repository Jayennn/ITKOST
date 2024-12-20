import psycopg2
from widgets.container import Container
from config.settings import Settings, FontLoader
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from components.index import Button, Input, Label
from PyQt6.QtCore import Qt
from database.conn import DatabaseConnection
from components.navbar import Navbar
from pages.register_page import RegisterPage
from config.session import set_user_info

class LoginPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow')

        # Load Fonts
        FontLoader.load_fonts()

        # Initialize database connection
        self.db = DatabaseConnection()

        # Initialize UI
        self.init_ui()


    def open_register_page(self):
        from pages.register_page import RegisterPage
        self.register_page = RegisterPage()
        self.register_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.register_page.show()
        self.destroy()

    def tenant_home_page(self):
        from pages.tenant.tenant_home_page import TenantHomePage
        self.tenant_home_page = TenantHomePage()
        self.tenant_home_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.tenant_home_page.show()
        self.destroy()

    def owner_dashboard_page(self):
        from pages.owner.owner_dashboard_page import OwnerDashboardPage
        self.owner_dashboard_page = OwnerDashboardPage()
        self.owner_dashboard_page.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        self.owner_dashboard_page.show()
        self.destroy()

    def validate_form(self):
        # Check if both phone number and password are filled
        is_valid = all([
            self.phone_number.text().strip(),
            self.password.text().strip(),
        ])
        self.button_login.setDisabled(not is_valid)

    def form_submit(self):
        # Collect input values
        phone_number = self.phone_number.text().strip()
        password = self.password.text().strip()

        with self.db as db:
            # Query to check if user exists with given credentials
            query = """
                SELECT id, name, role 
                FROM public.user 
                WHERE phone_number = %s AND password = %s
            """
            
            # Execute the query
            result = db.query(query, (phone_number, password))
            
            if result:
                user = db.cursor.fetchone()
                
                if user:
                    # Store user info in session
                    set_user_info(
                        user_id=user['id'],
                        username=user['name'],
                        role=user['role']
                    )

                    print(f"Logged in as: {user['name']}, Role: {user['role']}, user id: {user['id']}")

                    # Redirect user based on role
                    match user['role']:
                        case 'tenant':
                            self.tenant_home_page()
                        case 'owner':
                            self.owner_dashboard_page()
                        case _:
                            print(f'Unrecognized role: {user["role"]}')
                            QMessageBox.warning(
                                self,
                                "Login Failed", 
                                "Your role is not recognized."
                            )
                else:
                    # If no user found, show warning
                    print("No user found with this phone number or password.")
                    QMessageBox.warning(
                        self,
                        "Login Failed",
                        "Invalid phone number or password."
                    )

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Navbar with Register Button
        navbar = Navbar(self)
        navbar.button.setText('Register')
        navbar.button.clicked.connect(self.open_register_page)
        layout.addWidget(navbar)

        # Container Wrapper
        container = Container()

        # Heading
        heading = Label(
            'Welcome to ITKOST!',
            font_size=18,
            font_weights=Settings.FONT_WEIGHTS['bold']
        )
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setObjectName('heading')
        container.container_layout.addWidget(heading)

        # Subheading
        subheading = Label(
            'Login First!',
            font_size=10,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        subheading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subheading.setObjectName('subheading')
        container.container_layout.addWidget(subheading)

        container.container_layout.addSpacing(5)

        # Input Phone Number
        phone_number_label = Label('Nomor Handphone')
        self.phone_number = Input(placeholder='Nomor Handphone')
        self.phone_number.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(phone_number_label)
        container.container_layout.addWidget(self.phone_number)

        container.container_layout.addSpacing(5)

        # Input Password
        password_label = Label('Password')
        self.password = Input(placeholder='Password', password_mode=True)
        self.password.textChanged.connect(self.validate_form)
        container.container_layout.addWidget(password_label)
        container.container_layout.addWidget(self.password)

        container.container_layout.addSpacing(25)

        # Login Button
        self.button_login = Button('Login', 'btn_login')
        self.button_login.setDisabled(True)
        self.button_login.clicked.connect(self.form_submit)
        container.container_layout.addWidget(self.button_login)

        # Add container to the layout
        layout.addStretch()
        layout.addWidget(container.container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
