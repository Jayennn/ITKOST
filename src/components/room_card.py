from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from components.label import Label
from config.settings import Settings


class RoomCard(QWidget):
    def __init__(self, image_path, title, description, price="Rp. 10.000", *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main layout for the card
        self.setObjectName("wrapper_card")
        self.setStyleSheet("""
            #wrapper_card {
                border: 1px solid red;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(4)

        # Image section
        image_label = QLabel(self)
        image_label.setMinimumWidth (230)
        image_label.setMaximumHeight(150)
        image_label.setObjectName("room_card")
        image_label.setStyleSheet(
            """
                #room_card {
                border: 1px solid red;
                border-radius: 10px;
                background-color: #fff;
                padding: 10px;
                
            }
            """
        )
        image_label.setScaledContents(True)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("No Image")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        wrapper_type_widget = QWidget()
        wrapper_type = QHBoxLayout(wrapper_type_widget)
        wrapper_type.setContentsMargins(0, 0, 0, 0)
        type_label = Label(
            text="Type",
            font_size=9,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        type_label.setObjectName("type_label")
        wrapper_type.addWidget(type_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        wrapper_type.addItem(spacer)
        
        category_label = Label(
            text="Putra",
            font_size=9,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        category_label.setObjectName("category_label")
        wrapper_type.addWidget(category_label)

        layout.addWidget(wrapper_type_widget)
        
        # wrapper_information
        wrapper_information_widget = QWidget()
        wrapper_information = QHBoxLayout(wrapper_information_widget)
        wrapper_information.setContentsMargins(0, 0, 0, 0)

        # Title
        title_label = Label(
            text=title,
            font_size=10,
            font_weights=Settings.FONT_WEIGHTS['black']
        )
        title_label.setObjectName("title")
        wrapper_information.addWidget(title_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        wrapper_information.addItem(spacer)

        price_label = Label(
            text=price,
            font_size=9,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        price_label.setObjectName("price_label")
        wrapper_information.addWidget(price_label)
        
        layout.addWidget(wrapper_information_widget)
        # Description
        description_label = Label(
            text=description,
            font_size=9,
            font_weights=Settings.FONT_WEIGHTS['medium']
        )
        description_label.setObjectName("description")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        

        self.setLayout(layout)
