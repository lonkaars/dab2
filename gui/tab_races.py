import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class TabRaces(QWidget):
  def __init__(self, parent=None):
    super(TabRaces, self).__init__(parent)

    layout = QFormLayout()
    layout.addWidget(QLabel("hoi"))

    self.setLayout(layout)

