from PyQt6.QtWidgets import QLineEdit
from config.settings import Settings, FontLoader
from PyQt6.QtGui import QFont
class Input(QLineEdit):
  def __init__(self, placeholder="", password_mode=False, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setPlaceholderText(placeholder)

    FontLoader.load_fonts()

    if password_mode:
      self.setEchoMode(QLineEdit.EchoMode.Password)
    
    self.setFont(QFont(Settings.FONT_FAMILY, 8))
    self.setObjectName('input')
    # self.minimumHeight(40)

