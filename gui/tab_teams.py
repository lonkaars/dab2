import os
import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt

from split_view_layout import *

from dataclasses import dataclass

@dataclass
class DBTeam():
  id: int = 0
  name: str = ""

class TeamsModel(QAbstractTableModel):
  cursor: mariadb.Cursor
  calendar_id: int = 1

  _header = ["team name"]
  _data: [DBTeam] = []

  def update(self):
    self.beginResetModel()
    self.cursor.execute("select `ID`, `teamName` from `teams` where `calendarID` = ?", (self.calendar_id,))
    self._data = list()
    for result in self.cursor.fetchall():
      self._data.append(DBTeam(*result))
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
      team = self._data[index.row()]
      return (
        team.name,
      )[index.column()]

  def set_calendar_id(self, calendar_id):
    self.calendar_id = calendar_id
    self.update()

class TeamBrowser(QTableView):
  model_table: TeamsModel
  model_proxy: QSortFilterProxyModel
  parent_update_fn: callable
  selected_team_id: int = 1
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

  def set_calendar_id(self, calendar_id):
    self.model_table.set_calendar_id(calendar_id)

  def on_selection(self):
    if self.ignore_update: return
    rows = self.selectionModel().selectedRows()
    if len(rows) == 0: return
    row = rows[0].row()
    self.temp_selection_index = row
    index = self.model_proxy.mapToSource(self.model_proxy.index(row, 0))
    new_team_id = self.model_table.headerData(index.row(), Qt.Vertical, Qt.DisplayRole)
    if self.selected_team_id == new_team_id: return
    self.selected_team_id = new_team_id
    self.parent_update()

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(TeamBrowser, self).__init__(parent)

    self.cursor = cursor

    self.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.model_table = TeamsModel(self.cursor)
    self.model_proxy = QSortFilterProxyModel()
    self.model_proxy.setSourceModel(self.model_table)
    self.setModel(self.model_proxy)
    self.setSortingEnabled(True)
    self.selectionModel().selectionChanged.connect(self.on_selection)
    self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class TeamDetailsWidget(QWidget):
  parent: QWidget
  cursor: mariadb.Cursor
  parent_update_fn: callable
  selected_team_id: int = 1

  team_members: QFormLayout
  layout: QVBoxLayout
  new_member_picker: QComboBox

  def member_remove(self):
    id = self.sender().property("id")
    self.cursor.execute("delete from `formula1`.`teamsmember` where `memberID` = ? and `teamsID` = ?", (id,self.selected_team_id,))
    self.update(False)

  def member_add(self, id):
    self.cursor.execute("insert into `formula1`.`teamsmember` (`memberID`, `teamsID`) values (?, ?)", (id,self.selected_team_id,))
    self.update(False)

  def update(self, cascade=True):
    for x in range(self.team_members.rowCount()):
      self.team_members.removeRow(0)
    self.cursor.execute("select member.ID, firstName, middleName, lastName from member join teamsmember on teamsmember.memberID = member.ID where teamsmember.teamsID = ?", (self.selected_team_id,))
    for member in self.cursor.fetchall():
      id = member[0]
      name = " ".join(member[1:4])
      remove_button = QPushButton("remove")
      remove_button.setProperty("id", id)
      remove_button.clicked.connect(self.member_remove)
      self.team_members.addRow(QLabel(name), remove_button)

    self.cursor.execute("select member.ID, firstName, middleName, lastName from member")
    self.new_member_picker.clear()
    for member in self.cursor.fetchall():
      self.new_member_picker.addItem(" ".join(member[1:4]), member[0])

    if cascade == False: return
    self.nationality_editor.update()

  def parent_update(self):
    if self.parent_update_fn != None:
      self.parent_update_fn()

  def set_team_id(self, id):
    self.selected_team_id = id
    self.update(False)

  def set_parent_update(self, fn):
    self.parent_update_fn = fn

  def __init__(self, cursor: mariadb.Cursor, parent=None):
    super(TeamDetailsWidget, self).__init__(parent)
    self.parent = parent
    self.cursor = cursor

    self.layout = QVBoxLayout(self)
    self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    self.layout.addWidget(QLabel("Team members"))

    self.team_members = QFormLayout(self)
    self.team_members.addRow("bernard", QPushButton("remove"))
    self.layout.addLayout(self.team_members)

    self.new_member_picker = QComboBox()
    self.new_member_picker.setCurrentIndex(-1)
    self.new_member_picker.setPlaceholderText("Add member...")
    self.new_member_picker.currentIndexChanged.connect(lambda i: self.member_add(self.new_member_picker.itemData(i)))
    self.layout.addWidget(self.new_member_picker)

    self.setLayout(self.layout)

class TabTeams(QWidget):
  parent: QMainWindow
  layout: SplitViewLayout
  cursor: mariadb.Cursor
  selected_team_id: int = 1
  calendar_id: int = 1

  team_browser: TeamBrowser
  team_details: TeamDetailsWidget

  def update(self, cascade=True):
    print("update TabTeams")

    if not cascade: return
    self.team_browser.update(True)

  def child_update(self):
    self.selected_team_id = self.team_browser.selected_team_id
    self.team_browser.update(False)
    self.team_details.set_team_id(self.selected_team_id)

  def set_calendar_id(self, calendar_id):
    self.calendar_id = calendar_id
    self.team_browser.set_calendar_id(calendar_id)

  def __init__(self, cursor, parent=None):
    super(TabTeams, self).__init__(parent)
    self.parent = parent
    self.layout = SplitViewLayout(self)
    self.cursor = cursor

    self.team_browser = TeamBrowser(self.cursor, self)
    self.team_browser.set_parent_update(self.child_update)
    self.layout.leftWidget(self.team_browser)

    self.team_details = TeamDetailsWidget(self.cursor, self)
    self.team_details.set_parent_update(self.child_update)
    self.layout.rightWidget(self.team_details)

    self.setLayout(self.layout)

