CREATE 
VIEW `formula1`.`vwcalendar` AS
SELECT 
	`calendar`.`year` AS `year`,
	`racedate`.`week` AS `week`,
	`racedate`.`date` AS `date`,
	`circuit`.`name` AS `name`
FROM
	(((`calendar`
	JOIN `racedate` ON ((`calendar`.`ID` = `racedate`.`calanderID`)))
	JOIN `racedatecircuit` ON ((`racedate`.`ID` = `racedatecircuit`.`raceDateID`)))
	JOIN `circuit` ON ((`racedatecircuit`.`circuitID` = `circuit`.`ID`)));


CREATE 
VIEW `formula1`.`vwteamcoureurs` AS	
SELECT 
	`calendar`.`ID` AS `ID`,
	`teams`.`teamNumber` AS `teamNumber`,
	`teams`.`teamName` AS `teamName`,
	`member`.`firstName` AS `firstName`,
	`member`.`middleName` AS `middleName`,
	`member`.`lastName` AS `lastName`
FROM
	(((`calander`
	JOIN `teams` ON ((`calendar`.`ID` = `teams`.`calanderID`)))
	JOIN `teamsmember` ON ((`teams`.`ID` = `teamsmember`.`teamsID`)))
	JOIN `member` ON ((`teamsmember`.`memberID` = `member`.`ID`)));
