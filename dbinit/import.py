#!/bin/python3

import os
import sys
import ergast_py
from dataclasses import dataclass
from datetime import datetime, date

e = ergast_py.Ergast()
id_key_map = dict()

set_calendar = list()
set_circuit = list()
set_function = list()
set_member = list()
set_specialposition = list()
set_endposition = list()
set_racetype = list()
set_racedate = list()
set_race = list()
set_nationality = list()
set_membernationality = list()
set_teams = list()
set_raceresult = list()

def race2id(race):
  return f"{race.date.timestamp()}-{race.circuit.circuit_id}"

def result2id(result):
  return f"{result.driver.driver_id}-{result.number}-{result.status}"

def team2id(team):
  return f"{team.calendar_id}-{team.id}"

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
  _calendar_id: int
  _race_type_id: str
  week: int
  date: datetime
  _circuit_id: str

@dataclass
class F1Member():
  id: str
  first_name: str
  middle_name: str
  last_name: str
  nationality: str
  _function: str
  _team_id: str

@dataclass
class F1EndPosition():
  _id: str
  _member_id: str
  position: int
  _status_id: int

@dataclass
class F1RaceResult():
  _end_position_id: str
  _race_id: str
  fastest_lap: int

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
  out = "insert into `formula1`.`member` (`firstName`, `middleName`, `lastName`, `functionID`) values "
  found_ids = set()
  for member in set_member:
    id = get_id_by_key_value("member", member.id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"(\"{member.first_name}\", \"{member.middle_name}\", \"{member.last_name}\", {get_id_by_key_value('function', member._function)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_specialposition():
  out = "insert into `formula1`.`specialposition` (`type`) values "
  found_ids = set()
  for status in set_specialposition:
    id = get_id_by_key_value("specialposition", status.status_id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"('{status.status}'),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_endposition():
  out = "insert into `formula1`.`endposition` (`memberID`, `position`, `specialPositionID`) values "
  found_ids = set()
  for pos in set_endposition:
    id = get_id_by_key_value("endposition", pos._id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({get_id_by_key_value('driver', pos._member_id)}, {pos.position}, {get_id_by_key_value('specialposition', pos._status_id)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

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
    out += f"({get_id_by_key_value('calendar', date._calendar_id)}, {get_id_by_key_value('racetype', date._race_type_id)}, {date.week}, \"{date.date.strftime('%Y-%m-%d')}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_race():
  out = "insert into `formula1`.`race` (`raceDateID`, `circuitID`) values "
  found_ids = set()
  for race in set_race:
    id = get_id_by_key_value("racedate", race.date)
    if id in found_ids: continue
    found_ids.add(id)
    id = get_id_by_key_value("race", race2id(race))
    out += f"({id}, {get_id_by_key_value('circuit', race.circuit.circuit_id)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_raceresult():
  out = "insert into `formula1`.`raceresult` (`endPositionID`, `raceID`, `fastestlap`) values "
  found_ids = set()
  for result in set_raceresult:
    end_position_id = get_id_by_key_value('endposition', result._end_position_id)
    race_id = get_id_by_key_value("race", result._race_id)
    out += f"({end_position_id}, {race_id}, {result.fastest_lap}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

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
    id = get_id_by_key_value("member", member.id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({id}, {get_id_by_key_value('nationality', member.nationality)}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_teams():
  out = "insert into `formula1`.`teams` (`calendarID`, `teamNumber`, `teamName`) values "
  found_ids = set()
  for team in set_teams:
    id = get_id_by_key_value("teams", team2id(team))
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({get_id_by_key_value('calendar', team.calendar_id)}, {team.number}, \"{team.name}\"),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

def export_teamsmember():
  out = "insert into `formula1`.`teamsmember` (`teamsID`, `memberID`) values "
  found_ids = set()
  for member in set_member:
    id = get_id_by_key_value("member", member.id)
    if id in found_ids: continue
    found_ids.add(id)
    out += f"({get_id_by_key_value('teams', member._team_id)}, {id}),"
  out = list(out)
  out[-1] = ";" # replace comma
  out = "".join(out)
  return out

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
    export_membernationality(),
    export_endposition(),
    export_teamsmember(),
    export_race(),
    export_raceresult()
  ]))

def crawl(year):
  set_racetype.append("first_practice")
  set_racetype.append("second_practice")
  set_racetype.append("third_practice")
  set_racetype.append("sprint")
  set_racetype.append("qualifying")
  set_racetype.append("normal")
  set_function.append("driver")
  for race in e.season(year).get_races():
    set_calendar.append(race.season)
    set_circuit.append(F1Circuit(
      race.circuit.circuit_id,
      race.circuit.circuit_name,
      0,
      len(race.laps)
    ))
    race = e.season(race.season).round(race.round_no).get_result()
    set_race.append(race)
    for result in race.results:
      for status in e.season(race.season).round(race.round_no).get_statuses():
        set_specialposition.append(status)
      end_position_id = result2id(result)
      set_endposition.append(F1EndPosition(
        end_position_id,
        result.driver.driver_id,
        result.position,
        result.status
      ))
      set_nationality.append(result.driver.nationality)
      team = F1Team(
        result.constructor.constructor_id,
        result.constructor.name,
        race.season,
        0
      )
      set_teams.append(team)
      set_member.append(F1Member(
        result.driver.driver_id,
        result.driver.given_name,
        "",
        result.driver.family_name,
        result.driver.nationality,
        "driver",
        team2id(team),
      ))
      if result.fastest_lap.time != None:
        set_raceresult.append(F1RaceResult(
          end_position_id,
          race2id(race),
          int((datetime.combine(date.min, result.fastest_lap.time) - datetime.min).total_seconds()),
        ))

    if race.first_practice != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "first_practice",
        race.first_practice.isocalendar()[1],
        race.first_practice,
        race.circuit.circuit_id
      ))
    if race.second_practice != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "second_practice",
        race.second_practice.isocalendar()[1],
        race.second_practice,
        race.circuit.circuit_id
      ))
    if race.third_practice != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "third_practice",
        race.third_practice.isocalendar()[1],
        race.third_practice,
        race.circuit.circuit_id
      ))
    if race.sprint != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "sprint",
        race.sprint.isocalendar()[1],
        race.sprint,
        race.circuit.circuit_id
      ))
    if race.qualifying != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "qualifying",
        race.qualifying.isocalendar()[1],
        race.qualifying,
        race.circuit.circuit_id
      ))
    if race.date != None:
      set_racedate.append(F1RaceDate(
        race.season,
        "normal",
        race.date.isocalendar()[1],
        race.date,
        race.circuit.circuit_id
      ))

if __name__ == "__main__":
  if len(sys.argv) < 2: # no year provided
    eprint("please provide a year to fetch f1 data from")
    exit(1)
  elif len(sys.argv) == 2: # crawl single year
    crawl(sys.argv[1])
  else: # crawl range
    for year in range(*[int(x) for x in sys.argv[1:4]]):
      crawl(year)
  export()

