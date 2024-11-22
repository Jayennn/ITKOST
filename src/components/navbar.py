from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QSpacerItem, 
    QSizePolicy
)
from config.settings import Settings, FontLoader
from components.index import Button, Label
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

class Navbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load Fonts
        FontLoader.load_fonts()

        # Initialize UI
        self.init_ui()



    def init_ui(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(20, 5, 20, 5)
        navbar_layout.setSpacing(10)
    
        brand_label = Label(
            'ITKOST',
            font_size=10, 
            font_weights=Settings.FONT_WEIGHTS['black']
        )

        navbar_layout.addWidget(brand_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        navbar_layout.addItem(spacer)


        self.button = Button('Login', 'navbar_button')
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setMinimumWidth(80)

        self.button.setDisabled(True)
        QTimer.singleShot(1000, lambda: self.button.setDisabled(False))
        


        navbar_layout.addWidget(self.button)

        self.setLayout(navbar_layout)

        self.setFixedHeight(60)
        
    