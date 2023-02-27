-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema formula1
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `formula1` ;

-- -----------------------------------------------------
-- Schema formula1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `formula1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `formula1` ;

-- -----------------------------------------------------
-- Table `formula1`.`calender`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`calender` ;

CREATE TABLE IF NOT EXISTS `formula1`.`calender` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `year` YEAR NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  UNIQUE INDEX `year_UNIQUE` (`year` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`circuit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`circuit` ;

CREATE TABLE IF NOT EXISTS `formula1`.`circuit` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `length` INT NULL DEFAULT NULL,
  `photo` MEDIUMBLOB NULL DEFAULT NULL,
  `laps` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`function`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`function` ;

CREATE TABLE IF NOT EXISTS `formula1`.`function` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `function` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`member`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`member` ;

CREATE TABLE IF NOT EXISTS `formula1`.`member` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NULL DEFAULT NULL,
  `middleName` VARCHAR(31) NULL DEFAULT NULL,
  `lastName` VARCHAR(45) NULL DEFAULT NULL,
  `photo` MEDIUMBLOB NULL DEFAULT NULL,
  `functionID` INT NULL DEFAULT NULL,
  `membercol` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `functionID_idx` (`functionID` ASC) VISIBLE,
  CONSTRAINT `functionID`
    FOREIGN KEY (`functionID`)
    REFERENCES `formula1`.`function` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`specialposition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`specialposition` ;

CREATE TABLE IF NOT EXISTS `formula1`.`specialposition` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`endposition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`endposition` ;

CREATE TABLE IF NOT EXISTS `formula1`.`endposition` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `memberID` INT NULL DEFAULT NULL,
  `position` INT NULL DEFAULT NULL,
  `specialPoistionID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `memberIDEndPosition_idx` (`memberID` ASC) VISIBLE,
  INDEX `specialPositionID_idx` (`specialPoistionID` ASC) VISIBLE,
  CONSTRAINT `memberIDEndPosition`
    FOREIGN KEY (`memberID`)
    REFERENCES `formula1`.`member` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `specialPositionID`
    FOREIGN KEY (`specialPoistionID`)
    REFERENCES `formula1`.`specialposition` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`fastestlap`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`fastestlap` ;

CREATE TABLE IF NOT EXISTS `formula1`.`fastestlap` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `memberID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `memberIDfastestlap_idx` (`memberID` ASC) VISIBLE,
  CONSTRAINT `memberIDfastestlap`
    FOREIGN KEY (`memberID`)
    REFERENCES `formula1`.`member` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`racetype`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`racetype` ;

CREATE TABLE IF NOT EXISTS `formula1`.`racetype` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `raceType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`racedate`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`racedate` ;

CREATE TABLE IF NOT EXISTS `formula1`.`racedate` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `calanderID` INT NULL DEFAULT NULL,
  `raceTypeID` INT NULL DEFAULT NULL,
  `week` INT NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `calanderID_idx` (`calanderID` ASC) VISIBLE,
  INDEX `raceTypeID_idx` (`raceTypeID` ASC) VISIBLE,
  CONSTRAINT `calanderID`
    FOREIGN KEY (`calanderID`)
    REFERENCES `formula1`.`calender` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `raceTypeID`
    FOREIGN KEY (`raceTypeID`)
    REFERENCES `formula1`.`racetype` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`race`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`race` ;

CREATE TABLE IF NOT EXISTS `formula1`.`race` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `raceDateID` INT NULL DEFAULT NULL,
  `raceNumber` INT NULL DEFAULT NULL,
  `fastestLapID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  UNIQUE INDEX `raceNumber_UNIQUE` (`raceNumber` ASC) VISIBLE,
  INDEX `raceDateID_idx` (`raceDateID` ASC) VISIBLE,
  INDEX `fastestLapID_idx` (`fastestLapID` ASC) VISIBLE,
  CONSTRAINT `fastestLapID`
    FOREIGN KEY (`fastestLapID`)
    REFERENCES `formula1`.`fastestlap` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `raceDateIDRace`
    FOREIGN KEY (`raceDateID`)
    REFERENCES `formula1`.`racedate` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`endpositionrace`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`endpositionrace` ;

CREATE TABLE IF NOT EXISTS `formula1`.`endpositionrace` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `endPositionID` INT NULL DEFAULT NULL,
  `raceID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `endPositionID_idx` (`endPositionID` ASC) VISIBLE,
  INDEX `raceID_idx` (`raceID` ASC) VISIBLE,
  CONSTRAINT `endPositionID`
    FOREIGN KEY (`endPositionID`)
    REFERENCES `formula1`.`endposition` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `raceID`
    FOREIGN KEY (`raceID`)
    REFERENCES `formula1`.`race` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`nationality`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`nationality` ;

CREATE TABLE IF NOT EXISTS `formula1`.`nationality` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `country` VARCHAR(45) NULL DEFAULT NULL,
  `flag` MEDIUMBLOB NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`membernationality`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`membernationality` ;

CREATE TABLE IF NOT EXISTS `formula1`.`membernationality` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `memberID` INT NULL DEFAULT NULL,
  `nationalityID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `memberID_idx` (`memberID` ASC) VISIBLE,
  INDEX `nationalityID_idx` (`nationalityID` ASC) VISIBLE,
  CONSTRAINT `memberIDNationality`
    FOREIGN KEY (`memberID`)
    REFERENCES `formula1`.`member` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `nationalityID`
    FOREIGN KEY (`nationalityID`)
    REFERENCES `formula1`.`nationality` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`racedatecircuit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`racedatecircuit` ;

CREATE TABLE IF NOT EXISTS `formula1`.`racedatecircuit` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `raceDateID` INT NULL DEFAULT NULL,
  `circuitID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `circuitID_idx` (`circuitID` ASC) VISIBLE,
  INDEX `raceDateID_idx` (`raceDateID` ASC) VISIBLE,
  CONSTRAINT `circuitID`
    FOREIGN KEY (`circuitID`)
    REFERENCES `formula1`.`circuit` (`ID`)
    ON UPDATE CASCADE,
  CONSTRAINT `raceDateID`
    FOREIGN KEY (`raceDateID`)
    REFERENCES `formula1`.`racedate` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`teams`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`teams` ;

CREATE TABLE IF NOT EXISTS `formula1`.`teams` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `calanderID` INT NULL DEFAULT NULL,
  `teamNumber` INT NULL DEFAULT NULL,
  `teamName` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `calanderID_idx` (`calanderID` ASC) VISIBLE,
  CONSTRAINT `calanderID2`
    FOREIGN KEY (`calanderID`)
    REFERENCES `formula1`.`calender` (`ID`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `formula1`.`teamsmember`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `formula1`.`teamsmember` ;

CREATE TABLE IF NOT EXISTS `formula1`.`teamsmember` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `teamsID` INT NULL DEFAULT NULL,
  `memberID` INT NULL DEFAULT NULL,
  `teamsMembercol` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE,
  INDEX `teamsID_idx` (`teamsID` ASC) VISIBLE,
  INDEX `memberIDteams_idx` (`memberID` ASC) VISIBLE,
  CONSTRAINT `memberIDteams`
    FOREIGN KEY (`memberID`)
    REFERENCES `formula1`.`member` (`ID`),
  CONSTRAINT `teamsID`
    FOREIGN KEY (`teamsID`)
    REFERENCES `formula1`.`teams` (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
