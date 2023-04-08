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
  return ""


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
  return ""


def export_racedatecircuit():
  return ""


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


def export_auditlog():
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
  for race in e.season(year).get_races():
    set_calendar.append(race.season)
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
    break

  print(set_teams)

  export()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("please provide a year to fetch f1 data from")
    exit(1)
  main(sys.argv[1])

