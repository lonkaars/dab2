import os
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from split_view_layout import *

class TabDrivers(QWidget):
  layout: SplitViewLayout

  def __init__(self, parent=None):
    super(TabDrivers, self).__init__(parent)

    layout = SplitViewLayout(self)
    layout.leftWidget(QLabel("hoi"))
    layout.rightWidget(QLabel("doei"))

    self.setLayout(layout)

