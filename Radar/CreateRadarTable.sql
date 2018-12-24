CREATE DATABASE `Radar`;

USE `Radar`;

CREATE TABLE `Radar` (
  `RadarID` int NOT NULL AUTO_INCREMENT,
  `CreatedDateTime` DATETIME(6),
  `State` VARCHAR(50),
  `URL` VARCHAR(100),
  PRIMARY KEY (`RadarID`)
);

CREATE UNIQUE INDEX `UQ_Radar_CreatedDateTime_State` ON `Radar`(`CreatedDateTime`, `State`);