CREATE DATABASE `Schedule`;

USE `Schedule`;

CREATE TABLE `Airline` (
  `AirlineID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100),
  `ICAOCode` VARCHAR(5),
  `IATACode` VARCHAR(5),
  PRIMARY KEY (`AirlineID`)
);

CREATE UNIQUE INDEX `UX_Airline_ICAOCode` ON `Airline`(`ICAOCode`);

CREATE TABLE `Flight` (
  `FlightID` INT NOT NULL AUTO_INCREMENT,
  `Number` VARCHAR(10),
  `ICAONumber` VARCHAR(15),
  `IATANumber` VARCHAR(15),
  PRIMARY KEY (`FlightID`)
);

CREATE UNIQUE INDEX `UX_Flight_ICAONumber` ON `Flight`(`ICAONumber`);

CREATE TABLE `Schedule` (
  `ScheduleID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(9),
  `Status` VARCHAR(10),
  `AirlineID` INT NOT NULL,
  `FlightID` INT NOT NULL,
  PRIMARY KEY (`ScheduleID`),
  FOREIGN KEY (`AirlineID`) REFERENCES `Airline`(`AirlineID`),
  FOREIGN KEY (`FlightID`) REFERENCES `Flight`(`FlightID`)
);

CREATE TABLE `Departure` (
  `ScheduleID` INT NOT NULL AUTO_INCREMENT,
  `ICAOCode` VARCHAR(5),
  `IATACode` VARCHAR(5),
  `Terminal` VARCHAR(10),
  `Gate` VARCHAR(10),
  `Delay` INT,
  `ScheduledTime` DATETIME(3),
  `EstimatedTime` DATETIME(3),
  `ActualTime` DATETIME(3),
  `EstimatedRunway` DATETIME(3),
  `ActualRunway` DATETIME(3),
  PRIMARY KEY (`ScheduleID`),
  FOREIGN KEY (`ScheduleID`) REFERENCES `Schedule`(`ScheduleID`)
);

CREATE INDEX `IX_Departure_ICAOCode_ScheduledTime` ON `Departure`(`ICAOCode`, `ScheduledTime`);
CREATE INDEX `IX_Departure_ICAOCode_ActualTime` ON `Departure`(`ICAOCode`, `ActualTime`);
CREATE INDEX `IX_Departure_ICAOCode_ActualRunway` ON `Departure`(`ICAOCode`, `ActualRunway`);

CREATE TABLE `Arrival` (
  `ScheduleID` INT NOT NULL AUTO_INCREMENT,
  `ICAOCode` VARCHAR(5),
  `IATACode` VARCHAR(5),
  `Terminal` VARCHAR(10),
  `Gate` VARCHAR(10),
  `Baggage` VARCHAR(10),
  `Delay` INT,
  `ScheduledTime` DATETIME(3),
  `EstimatedTime` DATETIME(3),
  `ActualTime` DATETIME(3),
  `EstimatedRunway` DATETIME(3),
  `ActualRunway` DATETIME(3),
  PRIMARY KEY (`ScheduleID`),
  FOREIGN KEY (`ScheduleID`) REFERENCES `Schedule`(`ScheduleID`)
);

CREATE INDEX `IX_Arrival_ICAOCode_ScheduledTime` ON `Arrival`(`ICAOCode`, `ScheduledTime`);
CREATE INDEX `IX_Arrival_ICAOCode_ActualTime` ON `Arrival`(`ICAOCode`, `ActualTime`);
CREATE INDEX `IX_Arrival_ICAOCode_ActualRunway` ON `Arrival`(`ICAOCode`, `ActualRunway`);
