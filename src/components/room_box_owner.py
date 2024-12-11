from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from components.label import Label
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from config.settings import FontLoader, Settings

class RoomBoxOwner(QWidget):
  def __init__(self, image_path, title, description=None, price=None, *args, **kwargs):
    """
    Create a room/property box for the owner view.
    :param image_path: Path to the image file.
    :param title: Title of the property.
    :param description: Description of the property (optional).
    :param price: Price of the property (optional).
    """
    super().__init__(*args, **kwargs)

    FontLoader.load_fonts()

    # Main layout for the box
    layout = QVBoxLayout(self)
    layout.setSpacing(15)
    self.setObjectName("box_item")
    self.setStyleSheet("""
        QWidget#box_item {
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 10px;
            max-width: 300px;
        }
    """)

    # Title of the property
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
    layout.addWidget(title_label)

    # Image placeholder
    image_label = QLabel()
    image_label.setMinimumWidth(230)
    image_label.setMaximumHeight(150)
    image_label.setStyleSheet("""
        border: 1px solid #cccccc;
        border-radius: 5px;
        background-color: #e0e0e0;
        text-align: center;
    """)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap(image_path)
    image_label.setPixmap(pixmap.scaled(230, 150, Qt.AspectRatioMode.KeepAspectRatio))
    image_label.setScaledContents(True)
    layout.addWidget(image_label)

    # Optional description
    if description:
        description_label = Label(
          description,
          font_size=10,
          font_weights=Settings.FONT_WEIGHTS["medium"]
        )
        layout.addWidget(description_label)

    # Optional price
    if price:
        price_label = Label(
          price,
          font_size=11,
          font_weights=Settings.FONT_WEIGHTS["bold"]
        )
        layout.addWidget(price_label)

    # Buttons for actions
    button_layout = QHBoxLayout()
    delete_button = QPushButton("Hapus Kost")
    delete_button.setStyleSheet("""
        QPushButton {
            background-color: #f9f9f9;
            border: 1px solid #d9534f;
            color: #d9534f;
            padding: 10px 8px;
            border-radius: 5px;
            font-size: 12px;
        }
    """)
    complete_button = QPushButton("Detail Kost")
    complete_button.setStyleSheet("""
        QPushButton {
            background-color: #F5F5FF;
            color: #101928;
            padding: 10px 8px;
            border-radius: 5px;
            font-size: 12px;
        }
    """)
    button_layout.addWidget(delete_button)
    button_layout.addWidget(complete_button)
    layout.addLayout(button_layout)
