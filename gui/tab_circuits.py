import os
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from split_view_layout import *

from dataclasses import dataclass

@dataclass
class DBCircuit():
  id: int = 0
  name: str = ""
  length: int = 0
  laps: int = 0
  photo: bytes = b""

class CircuitsModel(QAbstractTableModel):
  cursor: mariadb.Cursor
  calendar_id: int = 1

  _header = ["name", "length", "lap count"]
  _data: [DBCircuit] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select `ID`, `name`, `length`, `laps` from `circuit`")
    self._data = list()
    for result in self.cursor.fetchall():
      self._data.append(DBCircuit(*result))
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
      circuit = self._data[index.row()]
      return (
        circuit.name,
        circuit.length,
        circuit.laps,
      )[index.column()]

class CircuitBrowser(QTableView):
  model_table: CircuitsModel
  model_proxy: QSortFilterProxyModel
  parent_update_fn: callable
  selected_circuit_id: int = 1
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
    new_circuit_id = self.model_table.headerData(index.row(), Qt.Vertical, Qt.DisplayRole)
    if self.selected_circuit_id == new_circuit_id: return
    self.selected_circuit_id = new_circuit_id
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(CircuitBrowser, self).__init__(parent)

    self.cursor = cursor

    self.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_table = CircuitsModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_table)
    self.setModel(self.model_proxy)
    self.setSortingEnabled(True)
    self.selectionModel().selectionChanged.connect(self.on_selection)
    self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class CircuitDetailsWidget(QWidget):
  parent: QWidget
  cursor: mariadb.Cursor
  parent_update_fn: callable
  selected_circuit_id: int = 1

  layout: QVBoxLayout
  new_member_picker: QComboBox

  label_id: QLabel
  label_name: QLabel
  label_length: QLabel
  label_laps: QLabel
  label_map: QLabel

  def update(self, cascade=True):
    self.cursor.execute("select `ID`, `name`, `length`, `laps`, `photo` from `circuit` where `ID` = ?", (self.selected_circuit_id,))
    circuit = DBCircuit(*self.cursor.fetchone())

    self.label_id.setText(f"{circuit.id}")
    self.label_name.setText(f"{circuit.name}")
    self.label_length.setText(f"{circuit.length}m")
    self.label_laps.setText(f"{circuit.laps} laps")


    pixmap = QPixmap()
    pixmap.loadFromData(circuit.photo)
    self.label_map.setScaledContents(True)
    self.label_map.setPixmap(pixmap)
    if cascade == False: return

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_circuit_id(self, id):
    self.selected_circuit_id = id
    self.update(False)

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(CircuitDetailsWidget, self).__init__(parent)
    self.parent = parent
    self.cursor = cursor

    self.layout = QVBoxLayout(self)
    self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.layout.addWidget(QLabel("Circuit info"))

    self.label_id = QLabel("-")
    self.label_name = QLabel("-")
    self.label_length = QLabel("-")
    self.label_laps = QLabel("-")
    self.label_map = QLabel()

    form_grid = QFormLayout()
    form_grid.addRow(QLabel("ID:"), self.label_id)
    form_grid.addRow(QLabel("Name:"), self.label_name)
    form_grid.addRow(QLabel("Length:"), self.label_length)
    form_grid.addRow(QLabel("Laps:"), self.label_laps)
    self.layout.addLayout(form_grid)

    self.layout.addWidget(QLabel("Map"))
    self.layout.addWidget(self.label_map)

    self.setLayout(self.layout)

class TabCircuits(QWidget):
  parent: QMainWindow
  layout: SplitViewLayout
  cursor: mariadb.Cursor
  selected_circuit_id: int = 1

  circuit_browser: CircuitBrowser
  circuit_details: CircuitDetailsWidget

  def update(self, cascade=True):
    print("update TabCircuits")

    if not cascade: return
    self.circuit_browser.update(True)

  def child_update(self):
    self.selected_circuit_id = self.circuit_browser.selected_circuit_id
    self.circuit_browser.update(False)
    self.circuit_details.set_circuit_id(self.selected_circuit_id)

  def __init__(self, cursor, parent=None):
    super(TabCircuits, self).__init__(parent)
    self.parent = parent
    self.layout = SplitViewLayout(self)
    self.cursor = cursor

    self.circuit_browser = CircuitBrowser(self.cursor, self)
    self.circuit_browser.set_parent_update(self.child_update)
    self.layout.leftWidget(self.circuit_browser)

    self.circuit_details = CircuitDetailsWidget(self.cursor, self)
    self.circuit_details.set_parent_update(self.child_update)
    self.layout.rightWidget(self.circuit_details)

    self.setLayout(self.layout)

