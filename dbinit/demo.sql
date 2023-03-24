insert into `formula1`.`calendar` (`year`) values
	('2010'),
	('2011'),
	('2012'),
	('2013'),
	('2014');

insert into `formula1`.`circuit` (`name`, `length`, `laps`) values
	("Dolphin shoals", 2, 3),
	("Maple treeway", 4, 2),
	("Moo moo meadows", 6, 1);

insert into `formula1`.`function` (`function`) values
	("Driver"),
	("Concierge");

insert into `formula1`.`nationality` (`country`) values
	("Netherlands"),
	("Germany"),
	("United states of America"),
	("Japan"),
	("North Korea"),
	("Australië"),
	("Gelderland zuid");

insert into `formula1`.`racetype` (`raceType`) values
	("Qualification"),
	("Real deal race");

insert into `formula1`.`specialposition` (`type`) values
	("Disqualified"),
	("Did not finish");

insert into `formula1`.`member` (`firstName`, `middleName`, `lastName`, `functionID`) values
	("Mario", "", "Mario", 1),
	("Carlos", "Sainz", "jr.", 1),
	("Max", "", "Verstappen", 1),
	("Loek", "Le", "Blansch", 2);

insert into `formula1`.`racedate` (`calendarID`, `raceTypeID`, `week`, `date`) values
	(2, 2, 4, "2011-01-29"),
	(1, 2, 12, "2011-04-02"),
	(3, 1, 28, "2011-07-25"),
	(5, 1, 29, "2011-07-26");

insert into `formula1`.`teams` (`calendarID`, `teamNumber`, `teamName`) values
	(1, 1, "Team red"),
	(2, 2, "Team blue");

insert into `formula1`.`endposition` (`memberID`, `position`, `specialPositionID`) values
	(1, 3, NULL),
	(2, 2, NULL),
	(3, 4, NULL),
	(4, 1, NULL);

insert into `formula1`.`fastestlap` (`memberID`) values (1), (2), (3), (4);

insert into `formula1`.`membernationality` (`memberID`, `nationalityID`) values
	(1, 1),
	(2, 4),
	(3, 5),
	(4, 3);

insert into `formula1`.`racedatecircuit` (`raceDateID`, `circuitID`) values
	(1, 3),
	(2, 2),
	(3, 1),
	(4, 1);

insert into `formula1`.`teamsmember` (`teamsID`, `memberID`) values
	(1, 1),
	(1, 2),
	(2, 3),
	(2, 4);

insert into `formula1`.`race` (`raceDateID`, `raceNumber`, `fastestLapID`) values
	(1, 1, 1),
	(1, 2, 2),
	(2, 1, 3),
	(2, 2, 2),
	(2, 3, 4),
	(3, 1, 1),
	(3, 2, 2),
	(4, 1, 4),
	(4, 2, 2);

insert into `formula1`.`endpositionrace` (`endPositionID`, `raceID`) values
	(1, 2),
	(3, 4),
	(4, 1),
	(3, 2),
	(3, 3);

