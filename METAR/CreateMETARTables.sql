CREATE DATABASE `METAR`;

USE `METAR`;

CREATE TABLE `METAR` (
  `METARID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(5),
  `Mode` VARCHAR(4),
  `StationID` VARCHAR(4),
  `Time` DATETIME(0),
  `Cycle` INT,
  `WindDirection` DECIMAL(5, 2),
  `WindSpeed` DECIMAL(5, 2),
  `WindGust` DECIMAL(5, 2),
  `WindDirectionFrom` DECIMAL(5, 2),
  `WindDirectionTo` DECIMAL(5, 2),
  `Visibility` DECIMAL(5, 2),
  `VisibilityDirection` DECIMAL(5, 2),
  `MaxVisibility` DECIMAL(5, 2),
  `MaxVisibilityDirection` DECIMAL(5, 2),
  `Temperature` DECIMAL(5, 2),
  `DewPoint` DECIMAL(5, 2),
  `Pressure` DECIMAL(5, 2),
  `SeaLevelPressure` DECIMAL(6, 2),
  `PeakWindSpeed` DECIMAL(5, 2),
  `PeakWindDirection` DECIMAL(5, 2),
  `MaxTemperature6Hr` DECIMAL(5, 2),
  `MinTemperature6Hr` DECIMAL(5, 2),
  `MaxTemperature24Hr` DECIMAL(5, 2),
  `MinTemperature24Hr` DECIMAL(5, 2),
  `Precipitation1Hr` DECIMAL(5, 2),
  `Precipitation3Hr` DECIMAL(5, 2),
  `Precipitation6Hr` DECIMAL(5, 2),
  `Precipitation24Hr` DECIMAL(5, 2),
  `Code` VARCHAR(500),
  PRIMARY KEY (`METARID`)
);

CREATE UNIQUE INDEX `UQ_METAR_StationID_Time` ON `METAR`(`StationID`, `Time`);

CREATE TABLE `RunwayVisibility` (
  `RunwayVisibilityID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Name` VARCHAR(20),
  `Low` DECIMAL(5, 2),
  `High` DECIMAL(5, 2),
  PRIMARY KEY (`RunwayVisibilityID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);

CREATE TABLE `PresentWeather` (
  `PresentWeatherID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Intensity` VARCHAR(2),
  `Descriptor` VARCHAR(2),
  `Precipitation` VARCHAR(2),
  `Obscuration` VARCHAR(2),
  `Other` VARCHAR(2),
  PRIMARY KEY (`PresentWeatherID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);

CREATE TABLE `RecentWeather` (
  `RecentWeatherID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Intensity` VARCHAR(2),
  `Descriptor` VARCHAR(2),
  `Precipitation` VARCHAR(2),
  `Obscuration` VARCHAR(2),
  `Other` VARCHAR(2),
  PRIMARY KEY (`RecentWeatherID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);

CREATE TABLE `SkyCondition` (
  `SkyConditionID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Cover` VARCHAR(3),
  `Height` DECIMAL(7, 2),
  `Cloud` VARCHAR(3),
  PRIMARY KEY (`SkyConditionID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);

CREATE TABLE `WindShearRunway` (
  `WindShearRunwayID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Runway` VARCHAR(20),
  PRIMARY KEY (`WindShearRunwayID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);

CREATE TABLE `Remark` (
  `RemarkID` INT NOT NULL AUTO_INCREMENT,
  `METARID` INT NOT NULL,
  `Remark` VARCHAR(200),
  PRIMARY KEY (`RemarkID`),
  FOREIGN KEY (`METARID`) REFERENCES `METAR`(`METARID`)
);