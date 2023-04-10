import mariadb
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from tab_drivers import *
from tab_teams import *
from tab_calendar import *
from tab_circuits import *
from tab_races import *

class MainWindow(QMainWindow):
  cursor: mariadb.Cursor = None
  db: mariadb.Connection = None
  menu_bar: QMenuBar

  _tab_drivers: TabDrivers
  _tab_teams: TabTeams
  _tab_calendar: TabCalendar
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

  def __init__(self, cursor: mariadb.Cursor, db: mariadb.Connection, parent=None):
    super(MainWindow, self).__init__(parent)

    self.set_cursor(cursor)
    self.set_connection(db)

    self.setWindowTitle("[floating] dab2 eindopdracht main window")
    self.setMinimumHeight(500)

    self._tab_drivers = TabDrivers(self.cursor, self)
    self._tab_teams = TabTeams(self)
    self._tab_calendar = TabCalendar(self)
    self._tab_circuits = TabCircuits(self)
    self._tab_races = TabRaces(self)

    main_layout = QTabWidget(self);
    main_layout.addTab(self._tab_drivers, "drivers")
    main_layout.addTab(self._tab_teams, "teams")
    main_layout.addTab(self._tab_calendar, "calendar")
    main_layout.addTab(self._tab_circuits, "cirucits")
    main_layout.addTab(self._tab_races, "races")
    
    self.menu_bar = QMenuBar(self)
    menu_procedures = self.menu_bar.addMenu("file")
    sp_update_flags = menu_procedures.addAction("Exit (commit changes)")
    sp_update_flags.triggered.connect(self.exit_commit)
    sp_update_flags = menu_procedures.addAction("Exit (don't commit changes)")
    sp_update_flags.triggered.connect(self.exit_no_commit)
    menu_procedures = self.menu_bar.addMenu("procedures")
    sp_update_flags = menu_procedures.addAction("Import/update flags")
    sp_update_flags.triggered.connect(self.call_update_flags)
    sp_update_persons = menu_procedures.addAction("Import/update driver portraits")
    sp_update_persons.triggered.connect(self.call_update_persons)
    sp_delete_flags = menu_procedures.addAction("Delete flags")
    sp_delete_flags.triggered.connect(self.call_delete_flags)
    menu_procedures = self.menu_bar.addMenu("database")
    sp_update_flags = menu_procedures.addAction("Commit changes")
    sp_update_flags.triggered.connect(self.commit)

    self.setMenuBar(self.menu_bar)
    self.setCentralWidget(main_layout)


