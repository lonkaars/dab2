import os
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class TabCircuits(QWidget):
  def __init__(self, parent=None):
    super(TabCircuits, self).__init__(parent)

    layout = QFormLayout()
    layout.addWidget(QLabel("hoi"))

    self.setLayout(layout)

