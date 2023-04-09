import os
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from split_view_layout import *

from dataclasses import dataclass

@dataclass
class DBDriver():
  id: int
  first_name: str
  last_name: str

class DriverModel(QAbstractTableModel):
  cursor: mariadb.Cursor

  _header = ["first name", "last name"]
  _data: [DBDriver] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select `ID`, `firstName`, `lastName` from `member`")
    self._data = list()
    for result in self.cursor.fetchall():
      self._data.append(DBDriver(*result))
    self.endResetModel()

  def __init__(self, cursor):
    super().__init__()
    self.cursor = cursor
    self.update()

  def rowCount(self, index=0):
    return len(self._data)

  def columnCount(self, index=0):
    return len(self._header)

  def headerData(self, section, orientation, role):
    if role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return self._header[section]
      else:
        return self._data[section].id

  def data(self, index, role):
    if role == Qt.DisplayRole:
      driver = self._data[index.row()]
      return (
        driver.first_name,
        driver.last_name,
      )[index.column()]

class DriverDetailsWidget(QWidget):
  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(DriverDetailsWidget, self).__init__(parent)

    layout = QVBoxLayout(self)
    # layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    label_portrait = QLabel("Driver portrait")
    layout.addWidget(label_portrait)

    details_form = QFormLayout(self)
    details_form.addRow("First name", QLineEdit("hoi"))
    details_form.addRow("Middle name", QLineEdit("hoi"))
    details_form.addRow("Last name", QLineEdit("hoi"))
    layout.addLayout(details_form)

    self.setLayout(layout)

class TabDrivers(QWidget):
  layout: SplitViewLayout
  cursor: mariadb.Cursor
  
  widget_driver_table: QTableView
  model_driver_table: DriverModel
  model_proxy: QSortFilterProxyModel

  driver_details: DriverDetailsWidget

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(TabDrivers, self).__init__(parent)
    self.cursor = cursor
    self.layout = SplitViewLayout(self)

    self.widget_driver_table = QTableView(self)
    self.widget_driver_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_driver_table = DriverModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_driver_table)
    self.widget_driver_table.setModel(self.model_proxy)
    self.widget_driver_table.setSortingEnabled(True)
    self.layout.leftWidget(self.widget_driver_table)

    self.driver_details = DriverDetailsWidget(self)
    self.layout.rightWidget(self.driver_details)

    self.setLayout(self.layout)

