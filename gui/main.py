#!/bin/python3

import sys
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import *

from login_dialog import *
from main_window import *

if __name__ == '__main__':
  app = QApplication(sys.argv)
  login_dialog = LoginDialog()
  db = None
  while True:
    login_dialog.exec()
    try:
      db = mariadb.connect(host=login_dialog.hostname, user=login_dialog.username, password=login_dialog.password, database=login_dialog.database)
      break
    except:
      print("Login failed, please try again")
  win = MainWindow(db.cursor(buffered=True), db)
  win.show()
  app.exec()

