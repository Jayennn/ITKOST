import PyQt6.QtCore
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont, QIcon
from config.settings import FontLoader, Settings

class Button(QPushButton):
    def __init__(self, text, name="", icon=None, *args, **kwargs):
      super().__init__(*args, **kwargs)

      # Load styles from CSS
      with open('./src/styles/components/button.css', 'r') as file:
          self.setStyleSheet(file.read())

      # Set button text
      self.setText(text)
      
      # Load and apply fonts
      FontLoader.load_fonts()
      font = QFont(Settings.FONT_FAMILY, 8)
      font.setWeight(Settings.FONT_WEIGHTS["medium"])
      self.setFont(font)

      # Set icon if provided
      if icon is not None:
          self.setIcon(icon)
          self.setIconSize(PyQt6.QtCore.QSize(16, 16))  # Adjust icon size


      # Set object name and size
      self.setObjectName(name)
      self.setMinimumHeight(30)
