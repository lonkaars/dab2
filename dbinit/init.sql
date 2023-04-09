create schema if not exists `formula1`;

create table if not exists `formula1`.`calendar` (
  `ID` int not null auto_increment,
  `year` year not null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  unique index `year_UNIQUE` (`year` asc) visible);

create table if not exists `formula1`.`circuit` (
  `ID` int not null auto_increment,
  `name` varchar(45) null default null,
  `length` int null default null,
  `photo` mediumblob null default null,
  `laps` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

create table if not exists `formula1`.`function` (
  `ID` int not null auto_increment,
  `function` varchar(45) null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

create table if not exists `formula1`.`member` (
  `ID` int not null auto_increment,
  `firstName` varchar(45) null default null,
  `middleName` varchar(31) null default null,
  `lastName` varchar(45) null default null,
  `photo` mediumblob null default null,
  `functionID` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `functionID_idx` (`functionID` asc) visible,
  constraint `functionID`
    foreign key (`functionID`)
    references `formula1`.`function` (`ID`)
    on update cascade);

create table if not exists `formula1`.`specialposition` (
  `ID` int not null auto_increment,
  `type` varchar(45) null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

create table if not exists `formula1`.`endposition` (
  `ID` int not null auto_increment,
  `memberID` int null default null,
  `position` int null default null,
  `specialPositionID` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `memberIDEndPosition_idx` (`memberID` asc) visible,
  index `specialPositionID_idx` (`specialPositionID` asc) visible,
  constraint `memberIDEndPosition`
    foreign key (`memberID`)
    references `formula1`.`member` (`ID`)
    on update cascade,
  constraint `specialPositionID`
    foreign key (`specialPositionID`)
    references `formula1`.`specialposition` (`ID`)
    on update cascade);

create table if not exists `formula1`.`racetype` (
  `ID` int not null auto_increment,
  `raceType` varchar(45) not null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

create table if not exists `formula1`.`racedate` (
  `ID` int not null auto_increment,
  `calendarID` int null default null,
  `raceTypeID` int null default null,
  `week` int not null,
  `date` date not null,
  primary key (`ID`),
  index `calendarID_idx` (`calendarID` asc) visible,
  index `raceTypeID_idx` (`raceTypeID` asc) visible,
  constraint `calendarID`
    foreign key (`calendarID`)
    references `formula1`.`calendar` (`ID`)
    on update cascade,
  constraint `raceTypeID`
    foreign key (`raceTypeID`)
    references `formula1`.`racetype` (`ID`)
    on update cascade);

create table if not exists `formula1`.`race` (
  `ID` int not null auto_increment,
  `raceDateID` int null default null,
  `circuitID` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `circuitID_idx` (`circuitID` asc) visible,
  index `raceDateID_idx` (`raceDateID` asc) visible,
  constraint `circuitID`
    foreign key (`circuitID`)
    references `formula1`.`circuit` (`ID`)
    on update cascade,
  constraint `raceDateID`
    foreign key (`raceDateID`)
    references `formula1`.`racedate` (`ID`)
    on update cascade);

create table if not exists `formula1`.`raceresult` (
  `ID` int not null auto_increment,
  `endPositionID` int null default null,
  `raceID` int null default null,
  `fastestlap` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `endPositionID_idx` (`endPositionID` asc) visible,
  index `raceID_idx` (`raceID` asc) visible,
  constraint `endPositionID`
    foreign key (`endPositionID`)
    references `formula1`.`endposition` (`ID`)
    on update cascade,
  constraint `raceID`
    foreign key (`raceID`)
    references `formula1`.`race` (`ID`)
    on update cascade);

create table if not exists `formula1`.`nationality` (
  `ID` int not null auto_increment,
  `country` varchar(45) null default null,
  `flag` mediumblob null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

create table if not exists `formula1`.`membernationality` (
  `ID` int not null auto_increment,
  `memberID` int null default null,
  `nationalityID` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `memberID_idx` (`memberID` asc) visible,
  index `nationalityID_idx` (`nationalityID` asc) visible,
  constraint `memberIDNationality`
    foreign key (`memberID`)
    references `formula1`.`member` (`ID`)
    on update cascade,
  constraint `nationalityID`
    foreign key (`nationalityID`)
    references `formula1`.`nationality` (`ID`)
    on update cascade);

create table if not exists `formula1`.`teams` (
  `ID` int not null auto_increment,
  `calendarID` int null default null,
  `teamNumber` int null default null,
  `teamName` varchar(45) null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `calendarID_idx` (`calendarID` asc) visible,
  constraint `calendarID2`
    foreign key (`calendarID`)
    references `formula1`.`calendar` (`ID`)
    on update cascade);

create table if not exists `formula1`.`teamsmember` (
  `ID` int not null auto_increment,
  `teamsID` int null default null,
  `memberID` int null default null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible,
  index `teamsID_idx` (`teamsID` asc) visible,
  index `memberIDteams_idx` (`memberID` asc) visible,
  constraint `memberIDteams`
    foreign key (`memberID`)
    references `formula1`.`member` (`ID`),
  constraint `teamsID`
    foreign key (`teamsID`)
    references `formula1`.`teams` (`ID`));

create table if not exists `formula1`.`auditlog` (
  `ID` int not null auto_increment,
	`timestamp` timestamp not null default current_timestamp(),
	`user` varchar(45) not null default user(),
	`action` varchar(10) not null,
	`fieldName` varchar(45) not null,
	`newData` varchar(45) null,
  primary key (`ID`),
  unique index `ID_UNIQUE` (`ID` asc) visible);

use `formula1`;	

set session transaction isolation level serializable;

