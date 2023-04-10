import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from tab_drivers import *
from tab_teams import *
from tab_circuits import *
from tab_races import *

class MainWindow(QMainWindow):
  cursor: mariadb.Cursor = None
  db: mariadb.Connection = None
  menu_bar: QMenuBar
  calendar_id: int

  _tab_drivers: TabDrivers
  _tab_teams: TabTeams
  _tab_circuits: TabCircuits
  _tab_races: TabRaces

  def set_cursor(self, cursor: mariadb.Cursor):
    self.cursor = cursor

  def set_connection(self, db: mariadb.Connection):
    self.db = db

  def commit(self):
    self.db.commit()

  def exit(self, commit=False):
    if commit: self.commit()
    self.db.close()
    self.close()

  def exit_no_commit(self):
    self.exit(False)
  def exit_commit(self):
    self.exit(True)

  def call_update_flags(self):
    folder = QFileDialog().getExistingDirectory(self, "Open directory", "/var/dab2/")
    self.cursor.execute("call spUpdateFlags(?)", (folder,))

  def call_update_persons(self):
    folder = QFileDialog().getExistingDirectory(self, "Open directory", "/var/dab2/")
    self.cursor.execute("call spUpdatePersons(?)", (folder,))

  def call_delete_flags(self):
    self.cursor.execute("call spDeleteFlags()")

  def update(self, cascade=True):
    if cascade == False: return
    self._tab_drivers.update()
    self._tab_teams.update()
    # self._tab_circuits.update()
    # self._tab_races.update()

  def switch_season(self):
    self.calendar_id = self.sender().property("id")
    self.update()

  def __init__(self, cursor: mariadb.Cursor, db: mariadb.Connection, parent=None):
    super(MainWindow, self).__init__(parent)

    self.set_cursor(cursor)
    self.set_connection(db)

    self.setWindowTitle("[floating] dab2 eindopdracht main window")
    self.setMinimumHeight(500)

    self._tab_drivers = TabDrivers(self.cursor, self)
    self._tab_teams = TabTeams(self.cursor, self)
    self._tab_circuits = TabCircuits(self)
    self._tab_races = TabRaces(self)

    main_layout = QTabWidget(self);
    main_layout.addTab(self._tab_drivers, "drivers")
    main_layout.addTab(self._tab_teams, "teams")
    main_layout.addTab(self._tab_circuits, "cirucits")
    main_layout.addTab(self._tab_races, "races")
    
    self.menu_bar = QMenuBar(self)
    menu = self.menu_bar.addMenu("file")
    action = menu.addAction("Exit (commit changes)")
    action.triggered.connect(self.exit_commit)
    action = menu.addAction("Exit (don't commit changes)")
    action.triggered.connect(self.exit_no_commit)
    menu = self.menu_bar.addMenu("procedures")
    action = menu.addAction("Import/update flags")
    action.triggered.connect(self.call_update_flags)
    action = menu.addAction("Import/update driver portraits")
    action.triggered.connect(self.call_update_persons)
    action = menu.addAction("Delete flags")
    action.triggered.connect(self.call_delete_flags)
    menu = self.menu_bar.addMenu("database")
    action = menu.addAction("Commit changes")
    action.triggered.connect(self.commit)

    menu = self.menu_bar.addMenu("seasons")
    group = QActionGroup(menu)
    group.setExclusive(True)
    self.cursor.execute("select ID, year from calendar")
    for i, season in enumerate(self.cursor.fetchall()):
      action = menu.addAction(str(season[1]))
      action.setProperty("id", season[0])
      action.triggered.connect(self.switch_season)
      action.setCheckable(True)
      if i == 0:
        action.setChecked(True)
        self.calendar_id = season[0]
      group.addAction(action)

    self.setMenuBar(self.menu_bar)
    self.setCentralWidget(main_layout)

