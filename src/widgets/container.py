from PyQt6.QtWidgets import QWidget, QVBoxLayout
class Container(QWidget): 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.container = QWidget()
    self.container.setObjectName('container')
    self.container_layout = QVBoxLayout()
    self.container.setLayout(self.container_layout)
    self.container.setFixedWidth(350)

