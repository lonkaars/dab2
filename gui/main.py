#!/bin/python3

import sys
import mariadb
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import *

from login_dialog import *

global db
global cursor

class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)
    self.setWindowTitle("[floating] dab2 eindopdracht main window")

if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = MainWindow()
  login_dialog = LoginDialog()
  db = None
  while True:
    login_dialog.exec()
    try:
      db = mariadb.connect(host=login_dialog.hostname, user=login_dialog.username, password=login_dialog.password, database=login_dialog.database)
      break
    except:
      print("Login failed, please try again")
  cursor = db.cursor(buffered=True)
  win.show()
  app.exec()
