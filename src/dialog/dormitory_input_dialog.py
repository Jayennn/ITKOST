import os
from PyQt6.QtWidgets import (
  QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from config.settings import Settings
from components.input import Input
from components.button import Button


class DormitoryInputDialog(QDialog):
  def __init__(self, dormitory_types, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Add/Edit Dormitory")
    self.setModal(True)
    self.setMinimumWidth(500)

    # Layout
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    self.setLayout(layout)

    # Input Fields
    self.name_input = Input(placeholder="Dormitory Name")
    self.address_input = Input(placeholder="Address")
    self.price_input = Input(placeholder="Price")
    self.total_room_input = Input(placeholder="Total Rooms")
    self.empty_room_input = Input(placeholder="Empty Rooms")
    self.type_selector = QComboBox()

    for types in dormitory_types:
        self.type_selector.addItem(types['name'], types['id'])

    self.image_label = QLabel()
    self.image_label.setFixedHeight(150)
    self.image_label.setStyleSheet("border: 1px solid #ccc;")
    self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.image_path = None

    upload_button = Button("Upload Image")
    upload_button.clicked.connect(self.upload_image)

    # Add Widgets to Layout
    layout.addWidget(QLabel("Dormitory Name:"))
    layout.addWidget(self.name_input)
    layout.addWidget(QLabel("Address:"))
    layout.addWidget(self.address_input)
    layout.addWidget(QLabel("Price:"))
    layout.addWidget(self.price_input)
    layout.addWidget(QLabel("Total Rooms:"))
    layout.addWidget(self.total_room_input)
    layout.addWidget(QLabel("Empty Rooms:"))
    layout.addWidget(self.empty_room_input)
    layout.addWidget(QLabel("Dormitory Type:"))
    layout.addWidget(self.type_selector)
    layout.addWidget(QLabel("Upload Image:"))
    layout.addWidget(self.image_label)
    layout.addWidget(upload_button)

    # Save Button
    save_button = Button("Save")
    save_button.clicked.connect(self.accept)
    layout.addWidget(save_button)

  def upload_image(self):
    """Handle image file selection and display."""
    file_dialog = QFileDialog(self)
    file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
    if file_path:
        # Ensure the assets folder exists
        upload_dir = "./src/assets/dormitory-picture"
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded image to the directory
        filename = os.path.basename(file_path)
        save_path = os.path.join(upload_dir, filename)
        with open(file_path, 'rb') as src_file:
            with open(save_path, 'wb') as dst_file:
                dst_file.write(src_file.read())

        # Update image_path and label
        self.image_path = save_path
        pixmap = QPixmap(save_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

  def get_inputs(self):
    """Retrieve input values."""
    return {
        "name": self.name_input.text(),
        "address": self.address_input.text(),
        "price": self.price_input.text(),
        "total_room": self.total_room_input.text(),
        "empty_room": self.empty_room_input.text(),
        "dorm_type_id": self.type_selector.currentData(),
        "image_path": self.image_path
    }
