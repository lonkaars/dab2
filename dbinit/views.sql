use `formula1`;

create view `formula1`.`vwcalendar` as
select
	`calendar`.`year` as `year`,
	`racedate`.`week` as `week`,
	`racedate`.`date` as `date`,
	`circuit`.`name` as `name`
from
	`racedate`
	join `calendar` on `calendar`.`ID` = `racedate`.`calendarID`
	join `race` on `race`.`raceDateID` = `racedate`.`ID`
	join `circuit` on `race`.`circuitID` = `circuit`.`ID`;

create view `formula1`.`vwteamcoureurs` as
select
	`calendar`.`ID` as `ID`,
	`teams`.`teamNumber` as `teamNumber`,
	`teams`.`teamName` as `teamName`,
	`member`.`firstName` as `firstName`,
	`member`.`middleName` as `middleName`,
	`member`.`lastName` as `lastName`
from
	`calendar`
	join `teams` on `calendar`.`ID` = `teams`.`calendarID`
	join `teamsmember` on `teams`.`ID` = `teamsmember`.`teamsID`
	join `member` on `teamsmember`.`memberID` = `member`.`ID`;
