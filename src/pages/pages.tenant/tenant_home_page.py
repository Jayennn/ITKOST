from config.settings import Settings, FontLoader
from database.conn import DatabaseConnection

class TenantHomePage(QWidget):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setObjectName('mainWindow')

    FontLoader.load_fonts()

    self.init_ui()
    self.conn = DatabaseConnection()
    self.conn.connection()
  
  def init_ui(self):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    self.setLayout(layout)

    navbar = Navbar(self)
    navbar.button.setText()

    layout.addStretch()
    layout.addStretch()