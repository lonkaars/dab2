#!/bin/python3

import os
import sys
import ergast_py
from dataclasses import dataclass
import datetime

e = ergast_py.Ergast()
id_key_map = dict()

set_calendar = list()
set_circuit = list()
set_function = list()
set_member = list()
set_specialposition = list()
set_endposition = list()
set_fastestlap = list()
set_racetype = list()
set_racedate = list()
set_race = list()
set_endpositionrace = list()
set_nationality = list()
set_membernationality = list()
set_racedatecircuit = list()
set_teams = list()
set_teamsmember = list()

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

@dataclass
class F1Circuit():
  id: str
  name: str
  length: int
  laps: int

@dataclass
class F1Team():
  id: str
  name: str
  calendar_id: int
  number: int

@dataclass
class F1RaceDate():
  calendar_id: int
  race_type_id: int
  week: int
  date: datetime.datetime
  _circuit_id: str

def get_id_by_key_value(key, value):
  if key not in id_key_map: id_key_map[key] = list()
  if value in id_key_map[key]: return id_key_map[key].index(value) + 1
  id_key_map[key].append(value)
  return len(id_key_map[key])

def export_calendar():
  out = "insert into `formula1`.`calendar` (`year`) values "
  found_ids = set()
  for year in set_calendar:
    id = get_id_by_key_value("calendar", year)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"('{year}'),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_circuit():
  out = "insert into `formula1`.`circuit` (`name`, `length`, `laps`) values "
  found_ids = set()
  for circuit in set_circuit:
    id = get_id_by_key_value("circuit", circuit.id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"(\"{circuit.name}\", {circuit.length}, {circuit.laps}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_function():
  out = "insert into `formula1`.`function` (`function`) values "
  found_ids = set()
  for fn in set_function:
    id = get_id_by_key_value("function", fn)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"(\"{fn}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_member():
  out = "insert into `formula1`.`member` (`firstName`, `lastName`, `functionID`) values "
  found_ids = set()
  function_id = get_id_by_key_value("function", "driver")
  for member in set_member:
    id = get_id_by_key_value("member", member.driver_id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"(\"{member.given_name}\", \"{member.family_name}\", {function_id}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_specialposition():
  out = "insert into `formula1`.`specialposition` (`type`) values "
  found_ids = set()
  for type in set_specialposition:
    id = get_id_by_key_value("specialposition", type)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"('{type}'),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_endposition():
  return ""

def export_fastestlap():
  return ""

def export_racetype():
  out = "insert into `formula1`.`racetype` (`raceType`) values "
  found_ids = set()
  for type in set_racetype:
    id = get_id_by_key_value("racetype", type)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"('{type}'),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_racedate():
  out = "insert into `formula1`.`racedate` (`calendarID`, `raceTypeID`, `week`, `date`) values "
  found_ids = set()
  for date in set_racedate:
    id = get_id_by_key_value("racedate", date.date)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({date.calendar_id}, {date.race_type_id}, {date.week}, \"{date.date.strftime('%Y-%m-%d')}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_race():
  return ""

def export_endpositionrace():
  return ""

def export_nationality():
  out = "insert into `formula1`.`nationality` (`country`) values "
  found_ids = set()
  for country in set_nationality:
    id = get_id_by_key_value("nationality", country)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"(\"{country}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_membernationality():
  out = "insert into `formula1`.`membernationality` (`memberID`, `nationalityID`) values "
  found_ids = set()
  for member in set_member:
    id = get_id_by_key_value("member", member.driver_id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({id}, {get_id_by_key_value('nationality', member.nationality)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_racedatecircuit():
  out = "insert into `formula1`.`racedatecircuit` (`raceDateID`, `circuitID`) values "
  found_ids = set()
  for date in set_racedate:
    id = get_id_by_key_value("racedate", date.date)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({id}, {get_id_by_key_value('circuit', date._circuit_id)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_teams():
  out = "insert into `formula1`.`teams` (`calendarID`, `teamNumber`, `teamName`) values "
  found_ids = set()
  for team in set_teams:
    id = get_id_by_key_value("teams", team.id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({team.calendar_id}, {team.number}, \"{team.name}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_teamsmember():
  return ""

def export():
  print(("\n").join([
    export_nationality(),
    export_function(),
    export_calendar(),
    export_circuit(),
    export_racetype(),
    export_specialposition(),
    export_member(),
    export_racedate(),
    export_teams(),
    export_fastestlap(),
    export_membernationality(),
    export_endposition(),
    export_teamsmember(),
    export_racedatecircuit(),
    export_race(),
    export_endpositionrace()
  ]))

def main(year):
  set_racetype.append("first_practice")
  set_racetype.append("second_practice")
  set_racetype.append("third_practice")
  set_racetype.append("sprint")
  set_racetype.append("qualifying")
  set_racetype.append("normal")
  set_specialposition.append("disqualified")
  set_specialposition.append("dnf")
  set_function.append("driver")
  set_calendar.append(year)
  # make id's accessible in following code
  export_racetype()
  export_specialposition()
  export_function()
  export_calendar()
  i = 0
  for race in e.season(year).get_races():
    set_race.append(race)
    set_circuit.append(F1Circuit(
      race.circuit.circuit_id,
      race.circuit.circuit_name,
      0,
      len(race.laps)
    ))
    for driver in e.season(race.season).round(race.round_no).get_drivers():
      set_nationality.append(driver.nationality)
      set_member.append(driver)
    for team in e.season(race.season).round(race.round_no).get_constructors():
      set_teams.append(F1Team(
        team.constructor_id,
        team.name,
        1,
        0
      ))

    if race.first_practice != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "first_practice"),
        race.first_practice.isocalendar()[1],
        race.first_practice,
        race.circuit.circuit_id
      ))
    if race.second_practice != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "second_practice"),
        race.second_practice.isocalendar()[1],
        race.second_practice,
        race.circuit.circuit_id
      ))
    if race.third_practice != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "third_practice"),
        race.third_practice.isocalendar()[1],
        race.third_practice,
        race.circuit.circuit_id
      ))
    if race.sprint != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "sprint"),
        race.sprint.isocalendar()[1],
        race.sprint,
        race.circuit.circuit_id
      ))
    if race.qualifying != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "qualifying"),
        race.qualifying.isocalendar()[1],
        race.qualifying,
        race.circuit.circuit_id
      ))
    if race.date != None:
      set_racedate.append(F1RaceDate(
        get_id_by_key_value("calendar", year),
        get_id_by_key_value("racetype", "normal"),
        race.date.isocalendar()[1],
        race.date,
        race.circuit.circuit_id
      ))
    i += 1
    if i == 3: break

  export()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    eprint("please provide a year to fetch f1 data from")
    exit(1)
  main(sys.argv[1])

