import os
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from split_view_layout import *

from dataclasses import dataclass

@dataclass
class DBRace():
  id: int = 0
  week: int = 0
  date: str = ""
  circuit: str = ""
  number: int = 0

class RacesModel(QAbstractTableModel):
  cursor: mariadb.Cursor
  calendar_id: int = 1

  _header = ["Week", "Date", "Circuit", "Number"]
  _data: [DBRace] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select race.ID, racedate.week, racedate.date, circuit.name, row_number() over (order by date) from race join racedate on race.raceDateID = racedate.ID join circuit on race.circuitID = circuit.ID where racedate.calendarID = ?", (self.calendar_id,))
    self._data = list()
    for result in self.cursor.fetchall():
      trans_res = list(result)
      trans_res[2] = trans_res[2].strftime('%Y-%m-%d')
      self._data.append(DBRace(*trans_res))
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
      race = self._data[index.row()]
      return (
        race.week,
        race.date,
        race.circuit,
        race.number,
      )[index.column()]

  def set_calendar_id(self, calendar_id):
    self.calendar_id = calendar_id
    self.update()

class RaceBrowser(QWidget):
  view: QTableView
  model_table: RacesModel
  model_proxy: QSortFilterProxyModel
  parent_update_fn: callable
  selected_race_id: int = 1
  ignore_update: bool = False
  temp_selection_index: int = 0

  def update(self, cascade=True):
    self.model_table.update()
    self.ignore_update = True
    self.view.selectRow(self.temp_selection_index)
    self.ignore_update = False

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def set_calendar_id(self, calendar_id):
    self.model_table.set_calendar_id(calendar_id)

  def on_selection(self):
    if self.ignore_update: return
    rows = self.view.selectionModel().selectedRows()
    if len(rows) == 0: return
    row = rows[0].row()
    self.temp_selection_index = row
    index = self.model_proxy.mapToSource(self.model_proxy.index(row, 0))
    new_race_id = self.model_table.headerData(index.row(), Qt.Vertical, Qt.DisplayRole)
    if self.selected_race_id == new_race_id: return
    self.selected_race_id = new_race_id
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(RaceBrowser, self).__init__(parent)

    self.cursor = cursor

    self.view = QTableView()
    self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_table = RacesModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_table)
    self.view.setModel(self.model_proxy)
    self.view.setSortingEnabled(True)
    self.view.selectionModel().selectionChanged.connect(self.on_selection)

    layout = QGridLayout();
    layout.addWidget(self.view)
    self.setLayout(layout)

@dataclass
class DBResult():
  id: int = 0
  driver: str = ""
  fastest_lap: int = 0
  position: int = 0
  status: str = ""

class ResultsModel(QAbstractTableModel):
  cursor: mariadb.Cursor
  race_id: int = 1

  _header = ["Driver", "Fastest lap [s]", "Endposition", "Status"]
  _data: [DBResult] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select raceresult.ID, regexp_replace(concat(member.firstName, ' ', member.middleName, ' ', member.lastName), '  *', ' ') as driver, raceresult.fastestlap, endposition.position, specialposition.type from raceresult join endposition on endposition.ID = raceresult.endPositionID join member on member.ID = endposition.memberID join specialposition on specialposition.ID = endposition.specialPositionID where raceresult.raceID = ? order by endposition.position", (self.race_id,))
    self._data = list()
    for result in self.cursor.fetchall():
      self._data.append(DBResult(*result))
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
      result = self._data[index.row()]
      return (
        result.driver,
        result.fastest_lap,
        result.position,
        result.status,
      )[index.column()]

  def set_race_id(self, race_id):
    self.race_id = race_id
    self.update()

class ResultBrowser(QWidget):
  view: QTableView
  model_table: ResultsModel
  model_proxy: QSortFilterProxyModel
  parent_update_fn: callable
  selected_result_id: int = 1
  ignore_update: bool = False
  temp_selection_index: int = 0

  def update(self, cascade=True):
    self.model_table.update()
    self.ignore_update = True
    self.view.selectRow(self.temp_selection_index)
    self.ignore_update = False

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def set_race_id(self, race_id):
    self.model_table.set_race_id(race_id)

  def on_selection(self):
    if self.ignore_update: return
    rows = self.view.selectionModel().selectedRows()
    if len(rows) == 0: return
    row = rows[0].row()
    self.temp_selection_index = row
    index = self.model_proxy.mapToSource(self.model_proxy.index(row, 0))
    new_result_id = self.model_table.headerData(index.row(), Qt.Vertical, Qt.DisplayRole)
    if self.selected_result_id == new_result_id: return
    self.selected_result_id = new_result_id
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(ResultBrowser, self).__init__(parent)

    self.cursor = cursor

    self.view = QTableView()
    self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_table = ResultsModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_table)
    self.view.setModel(self.model_proxy)
    self.view.setSortingEnabled(True)
    self.view.selectionModel().selectionChanged.connect(self.on_selection)

    layout = QGridLayout();
    layout.addWidget(self.view)
    self.setLayout(layout)

class ResultDetailsWidget(QWidget):
  cursor: mariadb.Cursor
  parent_update_fn: callable
  selected_result_id: int = 1

  result_details: DBResult

  label_id: QLabel
  num_end_position: QSpinBox
  combo_status: QComboBox
  num_fastest_lap_time: QSpinBox

  def update(self, cascade=True):
    self.cursor.execute("select endposition.position, specialposition.type, raceresult.fastestlap from endposition join raceresult on raceresult.endPositionID = endposition.ID join specialposition on specialposition.ID = endposition.specialPositionID where raceresult.ID = ?", (self.selected_result_id,))
    result = self.cursor.fetchone()

    self.label_id.setText(f"{self.selected_result_id}")
    self.num_end_position.setValue(result[0])
    self.combo_status.setCurrentText(result[1])
    self.num_fastest_lap_time.setValue(result[2])
    
    if cascade == False: return

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_result_id(self, id):
    self.selected_result_id = id
    self.update(False)

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def save_edits(self):
    fastest_lap = self.num_fastest_lap_time.value()
    end_position = self.num_end_position.value()
    special_position_id = self.combo_status.itemData(self.combo_status.currentIndex())

    self.cursor.execute("select endPositionID from raceresult where ID = ?", (self.selected_result_id,))
    endposition_id = self.cursor.fetchone()[0]

    self.cursor.execute("update `raceresult` set `fastestlap` = ? where `ID` = ?", (fastest_lap, self.selected_result_id,))
    self.cursor.execute("update `endposition` set `position` = ?, `specialPositionID` = ? where `ID` = ?", (end_position, special_position_id, endposition_id,))

    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(ResultDetailsWidget, self).__init__(parent)
    self.cursor = cursor

    self.result_details = DBResult()

    layout = QVBoxLayout(self)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.label_id = QLabel("hoi")
    self.num_end_position = QSpinBox()
    self.num_end_position.setMinimum(0);
    self.num_end_position.setMaximum(25);
    self.num_end_position.setSingleStep(1);
    self.num_fastest_lap_time = QSpinBox()
    self.combo_status = QComboBox()

    self.cursor.execute("select ID, type from specialposition")
    for status in self.cursor.fetchall():
      self.combo_status.addItem(status[1], status[0])

    details_form = QFormLayout(self)
    details_form.addRow("ID", self.label_id)
    details_form.addRow("Fastest lap time (s)", self.num_fastest_lap_time)
    details_form.addRow("End position", self.num_end_position)
    details_form.addRow("Status", self.combo_status)
    layout.addLayout(details_form)

    self.push_button_save = QPushButton("Save edits")
    self.push_button_save.clicked.connect(self.save_edits)
    layout.addWidget(self.push_button_save)

    self.setLayout(layout)

class TabRaces(QWidget):
  calendar_id: int = 1
  parent: QMainWindow
  cursor: mariadb.Cursor
  selected_race_id: int = 1
  selected_race_result_id: int = 1

  race_browser: RaceBrowser
  result_browser: ResultBrowser
  result_editor: ResultDetailsWidget

  def set_calendar_id(self, calendar_id):
    self.calendar_id = calendar_id
    self.race_browser.set_calendar_id(calendar_id)

  def update(self, cascade=True):
    print("update TabRaces")

    if not cascade: return
    self.race_browser.update(True)

  def child_update(self):
    self.race_browser.update(False)
    self.selected_race_id = self.race_browser.selected_race_id
    self.result_browser.set_race_id(self.selected_race_id)
    self.selected_race_result_id = self.result_browser.selected_result_id
    self.result_editor.set_result_id(self.selected_race_result_id)

  def __init__(self, cursor, parent=None):
    super(TabRaces, self).__init__(parent)
    self.parent = parent
    self.cursor = cursor

    self.race_browser = RaceBrowser(self.cursor, self)
    self.result_browser = ResultBrowser(self.cursor, self)
    self.result_editor = ResultDetailsWidget(self.cursor, self)
    self.race_browser.set_parent_update(self.child_update)
    self.result_browser.set_parent_update(self.child_update)
    self.result_editor.set_parent_update(self.child_update)

    layout = QHBoxLayout()
    column1 = QVBoxLayout()
    column1.addWidget(QLabel("Race"))
    column1.addWidget(self.race_browser)
    column2 = QVBoxLayout()
    column2.addWidget(QLabel("Results"))
    column2.addWidget(self.result_browser)
    column3 = QVBoxLayout()
    column3.setAlignment(Qt.AlignmentFlag.AlignTop)
    column3.addWidget(QLabel("Details"))
    column3.addWidget(self.result_editor)
    layout.addLayout(column1)
    layout.addLayout(column2)
    layout.addLayout(column3)

    self.setLayout(layout)

