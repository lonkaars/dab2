import os
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from split_view_layout import *

from dataclasses import dataclass

@dataclass
class DBMember():
  id: int = 0
  first_name: str = ""
  middle_name: str = ""
  last_name: str = ""
  photo: bytes = b""

class DriverModel(QAbstractTableModel):
  cursor: mariadb.Cursor

  _header = ["first name", "middle name", "last name"]
  _data: [DBMember] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select `ID`, `firstName`, `middleName`, `lastName` from `member`")
    self._data = list()
    for result in self.cursor.fetchall():
      self._data.append(DBMember(*result))
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
        driver.middle_name,
        driver.last_name,
      )[index.column()]

class DriverBrowser(QTableView):
  model_table: DriverModel
  model_proxy: QSortFilterProxyModel
  parent_update_fn: callable
  selected_driver_id: int = 1
  ignore_update: bool = False
  temp_selection_index: int = 0

  def update(self, cascade=True):
    self.model_table.update()
    self.ignore_update = True
    self.selectRow(self.temp_selection_index)
    self.ignore_update = False

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def on_selection(self):
    if self.ignore_update: return
    rows = self.selectionModel().selectedRows()
    if len(rows) == 0: return
    row = rows[0].row()
    self.temp_selection_index = row
    index = self.model_proxy.mapToSource(self.model_proxy.index(row, 0))
    new_driver_id = self.model_table.headerData(index.row(), Qt.Vertical, Qt.DisplayRole)
    if self.selected_driver_id == new_driver_id: return
    self.selected_driver_id = new_driver_id
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(DriverBrowser, self).__init__(parent)

    self.cursor = cursor

    self.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_table = DriverModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_table)
    self.setModel(self.model_proxy)
    self.setSortingEnabled(True)
    self.selectionModel().selectionChanged.connect(self.on_selection)


class DriverDetailsWidget(QWidget):
  cursor: mariadb.Cursor
  parent_update_fn: callable
  selected_driver_id: int = 1

  driver_details: DBMember

  label_id: QLabel
  img_driver: QLabel
  line_edit_name_first: QLineEdit
  line_edit_name_middle: QLineEdit
  line_edit_name_last: QLineEdit
  push_button_save: QPushButton

  def update(self, cascade=True):
    self.cursor.execute("select `ID`, `firstName`, `middleName`, `lastName`, `photo` from `member` where `ID` = ?", (self.selected_driver_id,))
    self.driver_details = DBMember(*self.cursor.fetchone())

    pixmap = QPixmap()
    pixmap.loadFromData(self.driver_details.photo)
    self.label_id.setText(str(self.driver_details.id))
    self.img_driver.setScaledContents(True)
    # self.img_driver.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
    # self.img_driver.setPixmap(pixmap.scaled(self.img_driver.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.img_driver.setPixmap(pixmap)
    self.line_edit_name_first.setText(self.driver_details.first_name)
    self.line_edit_name_middle.setText(self.driver_details.middle_name)
    self.line_edit_name_last.setText(self.driver_details.last_name)

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_driver_id(self, id):
    self.selected_driver_id = id
    self.update(False)

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def save_edits(self):
    first_name = self.line_edit_name_first.text()
    middle_name = self.line_edit_name_middle.text()
    last_name = self.line_edit_name_last.text()
    self.cursor.execute("update `member` set `firstName` = ?, `middleName` = ?, `lastName` = ? where `ID` = ?", (first_name, middle_name, last_name, self.selected_driver_id,))
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(DriverDetailsWidget, self).__init__(parent)
    self.cursor = cursor

    self.driver_details = DBMember()

    layout = QVBoxLayout(self)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    label_portrait = QLabel("Driver portrait")
    self.img_driver = QLabel()
    layout.addWidget(label_portrait)
    layout.addWidget(self.img_driver)

    details_form = QFormLayout(self)
    self.label_id = QLabel()
    self.line_edit_name_first = QLineEdit()
    self.line_edit_name_middle = QLineEdit()
    self.line_edit_name_last = QLineEdit()
    details_form.addRow("ID", self.label_id)
    details_form.addRow("First name", self.line_edit_name_first)
    details_form.addRow("Middle name", self.line_edit_name_middle)
    details_form.addRow("Last name", self.line_edit_name_last)
    layout.addLayout(details_form)

    self.push_button_save = QPushButton("Save edits")
    self.push_button_save.clicked.connect(self.save_edits)
    layout.addWidget(self.push_button_save)

    self.setLayout(layout)

class TabDrivers(QWidget):
  layout: SplitViewLayout
  cursor: mariadb.Cursor
  
  driver_browser: DriverBrowser
  driver_details: DriverDetailsWidget

  selected_driver_id: int = 1

  def update(self, cascade=True):
    print("update TabDrivers")

    if not cascade: return
    self.driver_browser.update(True)
    self.driver_details.update(True)

  def child_update(self):
    self.selected_driver_id = self.driver_browser.selected_driver_id
    self.driver_browser.update(False)
    self.driver_details.set_driver_id(self.selected_driver_id)

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(TabDrivers, self).__init__(parent)
    self.cursor = cursor
    self.layout = SplitViewLayout(self)

    self.driver_browser = DriverBrowser(self.cursor, self)
    self.driver_browser.set_parent_update(self.child_update)
    self.layout.leftWidget(self.driver_browser)

    self.driver_details = DriverDetailsWidget(self.cursor, self)
    self.driver_details.set_parent_update(self.child_update)
    self.layout.rightWidget(self.driver_details)

    self.setLayout(self.layout)

