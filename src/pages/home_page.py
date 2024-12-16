from config.settings import FontLoader
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from components.navbar import Navbar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from config.settings import Settings, FontLoader
from pages.login_page import LoginPage
from components.button import Button
from components.label import Label
from dialog.select_role import SelectRole

class HomePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow') 

        FontLoader.load_fonts()

        self.init_ui()

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

        navbar = Navbar(self)
        navbar.button.clicked.connect(self.open_login_page)
        layout.addWidget(navbar)

        content_widget = QWidget()
        content_layout = QVBoxLayout()  
        content_widget.setLayout(content_layout)
        content_layout.setContentsMargins(20, 0, 20, 0)
        content_layout.addSpacing(15)

        title = Label(
            'Bingung Nyari Kos?',  
            font_size=24,         
            font_weights=Settings.FONT_WEIGHTS['black']
        )
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        content_layout.addWidget(title)

        text = Label(
            'KE ITKOST AJA',  
            font_size=12,     
            font_weights=Settings.FONT_WEIGHTS['semi-bold']
        )
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(text)

        image_label = QLabel()  
        pixmap = QPixmap('./src/assets/image.png')
        scaled_pixmap = pixmap.scaled(
            600, 300,  
            Qt.AspectRatioMode.KeepAspectRatio,  
            Qt.TransformationMode.SmoothTransformation  
        )
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(image_label)

        layout.addStretch()  
        layout.addWidget(content_widget)  
        layout.addStretch()  

        self.setLayout(layout)
