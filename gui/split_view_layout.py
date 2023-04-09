import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class SplitViewLayout(QGridLayout):
  def _setWidget(self, column: int, w: QWidget):
    self.addWidget(w, 0, column, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    return

  def leftWidget(self, w: QWidget):
    self._setWidget(0, w)

  def rightWidget(self, w: QWidget):
    self._setWidget(1, w)

  def __init__(self, parent=None):
    super(SplitViewLayout, self).__init__(parent)
    self.setColumnStretch(0, 1)
    self.setColumnMinimumWidth(0, 300)
    self.setColumnStretch(1, 0)
    self.setColumnMinimumWidth(1, 400)

