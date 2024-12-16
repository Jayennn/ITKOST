from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QLabel, 
    QStackedWidget, QGridLayout
)
from database.conn import DatabaseConnection
from PyQt6.QtCore import Qt
from config.settings import FontLoader, Settings
from components.label import Label
from components.room_box_owner import RoomBoxOwner
class OwnerDashboardPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow')

        # Load Fonts
        FontLoader.load_fonts()

        self.conn = DatabaseConnection()
        self.conn.connection()

        # Initialize UI
        self.init_ui()


    def switch_page(self, index):
        """Switch the main content page."""
        self.content_stack.setCurrentIndex(index)

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                color: white;
                min-width: 250px;
                max-width: 250px;
                border: 1px solid #E4E7EC;
            }
            QPushButton {
                background-color: #F5F5FF;
                color: #101928;
                padding: 10px 8px;
                text-align: left;
                font-weight: medium;
                font-size: 12px;
                border-radius: 5px;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        sidebar.setLayout(layout)

        # Add navigation buttons
        buttons = [
            ("Dashboard", 0),
            ("Kost", 1)
            # ("Properti Saya", 1),
            # ("Fitur Promosi", 2),
            # ("Laporan Statistik", 3),
            # ("Akun", 4),
        ]
        for text, index in buttons:
            button = QPushButton(f"  {text}")  # Add space for better alignment
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, idx=index: self.switch_page(idx))
            layout.addWidget(button)

        layout.addStretch()
        return sidebar

    def create_content_pages(self):
        """Create different pages for the content area."""
        self.content_stack = QStackedWidget()
        self.content_stack.setContentsMargins(20, 20, 20, 20)

        # Home Page
        home_page = self.create_home_page()
        self.content_stack.addWidget(home_page)

        # Property Management Page
        property_page = self.create_property_page()
        self.content_stack.addWidget(property_page)

        # Promotion Features Page
        promo_page = self.create_promo_page()
        self.content_stack.addWidget(promo_page)

        # Statistics Report Page
        stats_page = self.create_stats_page()
        self.content_stack.addWidget(stats_page)

        # Account Page
        account_page = self.create_account_page()
        self.content_stack.addWidget(account_page)

        return self.content_stack

    def create_home_page(self):
        """Create the Home page."""
        page = QFrame()
        layout = QVBoxLayout()

        page.setLayout(layout)
        heading = Label(
            "Halo, Guest",
            font_size=20,
            font_weights=Settings.FONT_WEIGHTS['bold']
        )

       
        layout.addWidget(heading)
        layout.addStretch()
        return page

    def handle_box_click(self):
        print("Box clicked!")

    def create_property_page(self):
        """Create the Property Management page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)

        heading = Label(
            "Tambahkan Data Kost",
            font_size=20,
            font_weights=Settings.FONT_WEIGHTS['bold']
        )
        layout.setSpacing(25)
        layout.addWidget(heading)
        
        query = '''
        SELECT dormitory.id AS dorm_id,
            dormitory.name AS dorm_name,
            public."user".name AS owner_name,
            public."user".phone_number
        FROM dormitory
        INNER JOIN public."user" ON dormitory.user_id = public."user".id;
        '''
        self.conn.cursor.execute(query)
        dormitories = self.conn.cursor.fetchall()
        # print(dormitories)
        for dorm in dormitories:
            dorm_id, dorm_name, owner_name, owner_number = dorm
            room_box = RoomBoxOwner(
                image_path="src/assets/placeholder-image.png",
                title=dorm_name,
                description="Kamar luas dengan fasilitas lengkap.",
                price="Rp. 500.000/Bulan"
            )
            layout.addWidget(room_box)

        

        layout.addStretch()
        return page

    def create_promo_page(self):
        """Create the Promotion Features page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)
        layout.addWidget(QLabel("Promotion Features Page"))
        return page

    def create_stats_page(self):
        """Create the Statistics Report page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)
        layout.addWidget(QLabel("Statistics Report Page"))
        return page

    def create_account_page(self):
        """Create the Account page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)
        layout.addWidget(QLabel("Account Management Page"))
        return page

    def init_ui(self):
        """Initialize the main UI layout."""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Main content area with stack
        content_stack = self.create_content_pages()
        main_layout.addWidget(content_stack)
