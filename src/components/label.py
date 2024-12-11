from PyQt6.QtWidgets import QLabel
from config.settings import Settings, FontLoader
from PyQt6.QtGui import QFont
class Label(QLabel):
  def __init__(self, text='', font_family=Settings.FONT_FAMILY, font_size=10, font_weights=Settings.FONT_WEIGHTS['medium'],*args, **kwargs):
    super().__init__(text, *args, **kwargs)
    self.setText(text)

    FontLoader.load_fonts()
    font = QFont(font_family, font_size, font_weights)
    self.setFont(font)
    self.setObjectName('label')

