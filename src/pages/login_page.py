import psycopg2
from widgets.container import Container
from config.settings import Settings, FontLoader
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from components.index import Button, Input, Label
from PyQt6.QtCore import Qt
from database.conn import DatabaseConnection
from components.navbar import Navbar
from pages.register_page import RegisterPage
from config.hashPassword import check_password
from config.session import set_user_info

class LoginPage(QWidget):
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setObjectName('mainWindow') 


            # Load Fonts
            FontLoader.load_fonts()

            # Initialize UI
            self.init_ui()


            self.conn = DatabaseConnection()
            self.conn.connection()

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
      
      def validate_form(self):
            is_valid=all([
                  self.phone_number.text().strip().strip(),
                  self.password.text().strip().strip(),
            ])

            self.button_login.setDisabled(not is_valid)
      def form_submit(self): 
            # TODO: Input Validation!
            
            value = {
                  'phone_number': self.phone_number.text(),
                  'password': self.password.text()
            }
            try:
                  query = "SELECT * FROM public.user WHERE phone_number= %s AND password=%s"
                  self.conn.cursor.execute(
                        query, 
                        (value['phone_number'], value['password'])
                  )
                  result = self.conn.cursor.fetchone()
                  if result:
                        user_name = result[1]
                        print("User exists:", result)
                        set_user_info(username=user_name, role='tenant') 
                        self.tenant_home_page()
                  else:
                        print("No user found with this phone number.")

            except psycopg2.Error as e:
                  print("Database Error: ", e)

      def init_ui(self):
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            self.setLayout(layout)
            
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

            # Button
            self.button_login = Button('Login', 'btn_login')
            self.button_login.setDisabled(True)
            self.button_login.clicked.connect(self.form_submit)
            container.container_layout.addWidget(self.button_login)
            
            layout.addStretch()
            layout.addWidget(container.container, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addStretch()