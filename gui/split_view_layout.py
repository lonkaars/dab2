import os
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class SplitViewLayout(QGridLayout):
  def leftWidget(self, w: QWidget):
    self.addWidget(w, 0, 0)

  def rightWidget(self, w: QWidget):
    self.addWidget(w, 0, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

  def __init__(self, parent=None):
    super(SplitViewLayout, self).__init__(parent)
    self.setColumnStretch(0, 1)
    self.setColumnMinimumWidth(0, 300)
    self.setColumnStretch(1, 0)
    self.setColumnMinimumWidth(1, 400)

