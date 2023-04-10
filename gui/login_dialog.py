import os
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class LoginDialog(QDialog):
  hostname = "localhost"
  username = os.getlogin()
  database = "formula1"
  password = ""
  field_database: QLineEdit
  field_hostname: QLineEdit
  field_username: QLineEdit
  field_password: QLineEdit

  def submit(self):
    self.database = self.field_database.text()
    self.hostname = self.field_hostname.text()
    self.username = self.field_username.text()
    self.password = self.field_password.text()
    if len(self.password) == 0: self.password = None
    self.close()
    return

  def __init__(self, parent=None):
    super(LoginDialog, self).__init__(parent)

    self.field_database = QLineEdit(self.database)
    self.field_database.setPlaceholderText("username")
    self.field_hostname = QLineEdit(self.hostname)
    self.field_hostname.setPlaceholderText("hostname")
    self.field_username = QLineEdit(self.username)
    self.field_username.setPlaceholderText("username")
    self.field_password = QLineEdit(self.password)
    self.field_password.setPlaceholderText("password")
    self.field_password.setEchoMode(QLineEdit.EchoMode.Password)
    self.login_button = QPushButton("Login")
    self.login_button.clicked.connect(self.submit)
    layout = QFormLayout()
    layout.addRow(QLabel("Database:"), self.field_database)
    layout.addRow(QLabel("Hostname:"), self.field_hostname)
    layout.addRow(QLabel("Username:"), self.field_username)
    layout.addRow(QLabel("Password:"), self.field_password)
    layout.addRow(self.login_button)

    self.setLayout(layout)

