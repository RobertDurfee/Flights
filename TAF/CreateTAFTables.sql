CREATE DATABASE `TAF`;

USE `TAF`;

/* TAF -||---O<- Group */
CREATE TABLE `TAF` (
  `TAFID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(5),
  `ICAOCode` VARCHAR(5),
  `OriginDateTime` DATETIME(0),
  `ValidFromDateTime` DATETIME(0),
  `ValidTillDateTime` DATETIME(0),
  `Form` VARCHAR(10),
  `Code` VARCHAR(2500),
  PRIMARY KEY (`TAFID`)
);

CREATE UNIQUE INDEX `UX_TAF_ICAOCode_OriginDateTime` ON `TAF`(`ICAOCode`, `OriginDateTime`)
CREATE INDEX `IX_TAF_ICAOCode_ValidFromDateTime_ValidTillDateTime` ON `TAF`(`ICAOCode`, `ValidFromDateTime`, `ValidTillDateTime`)
CREATE INDEX `IX_TAF_ICAOCode_ValidTillDateTime` ON `TAF`(`ICAOCode`, `ValidTillDateTime`)

/* TAF -||---O<- Group */
/* Group -||---O|- GroupHeader */
/* Group -||---O|- Wind */
/* Group -||---O|- Visibility */
/* Group -||---O<- Cloud */
/* Group -||---O|- VerticalVisibility */
/* Group -||---O<- Weather */
/* Group -||---O|- WindShear */
CREATE TABLE `Group` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `TAFID` INT NOT NULL,
  `Code` VARCHAR(500),
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`TAFID`) REFERENCES `TAF`(`TAFID`)
);

/* Group -||---O|- GroupHeader */
CREATE TABLE `GroupHeader` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(6),
  `Probability` INT,
  `FromDateTime` DATETIME(0),
  `TillDateTime` DATETIME(0),
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

CREATE INDEX `IX_GroupHeader_FromDateTime_TillDateTime` ON `GroupHeader`(`FromDateTime`, `TillDateTime`)
CREATE INDEX `IX_GroupHeader_TillDateTime` ON `GroupHeader`(`TillDateTime`)

/* Group -||---O|- Wind */
CREATE TABLE `Wind` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `Direction` VARCHAR(4),
  `Speed` INT,
  `Gust` INT,
  `Unit` VARCHAR(4),
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

/* Group -||---O|- Visibility */
CREATE TABLE `Visibility` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `MoreThan` BIT,
  `Range` VARCHAR(6),
  `Unit` VARCHAR(3),
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

/* Group -||---O<- Cloud */
CREATE TABLE `Cloud` (
  `CloudID` INT NOT NULL AUTO_INCREMENT,
  `GroupID` INT NOT NULL,
  `Layer` VARCHAR(5),
  `Ceiling` INT,
  `Type` VARCHAR(4),
  PRIMARY KEY (`CloudID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

/* Group -||---O|- VerticalVisibility */
CREATE TABLE `VerticalVisibility` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `VerticalVisibility` INT,
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

/* Group -||---O<- Weather */
/* Weather ->|---O<- Intensity */
/* Weather ->|---O<- Modifier */
/* Weather ->|---O<- Phenomenon */
CREATE TABLE `Weather` (
  `WeatherID` INT NOT NULL AUTO_INCREMENT,
  `GroupID` INT NOT NULL,
  PRIMARY KEY (`WeatherID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)

/* Weather ->|---O<- Intensity */
CREATE TABLE `Intensity` (
  `IntensityID` INT NOT NULL AUTO_INCREMENT,
  `Intensity` VARCHAR(3),
  PRIMARY KEY (`IntensityID`)
)

/* ->>---<<- */
CREATE TABLE `WeatherIntensity` (
  `WeatherID` INT NOT NULL,
  `IntensityID` INT NOT NULL,
  FOREIGN KEY (`WeatherID`) REFERENCES `Weather`(`WeatherID`),
  FOREIGN KEY (`IntensityID`) REFERENCES `Intensity`(`IntensityID`)
)

/* Weather ->|---O<- Modifier */
CREATE TABLE `Modifier` (
  `ModifierID` INT NOT NULL AUTO_INCREMENT,
  `Modifier` VARCHAR(3),
  PRIMARY KEY (`ModifierID`)
)

/* ->>---<<- */
CREATE TABLE `WeatherModifier` (
  `WeatherID` INT NOT NULL,
  `ModifierID` INT NOT NULL,
  FOREIGN KEY (`WeatherID`) REFERENCES `Weather`(`WeatherID`),
  FOREIGN KEY (`ModifierID`) REFERENCES `Modifier`(`ModifierID`)
)

/* Weather ->|---O<- Phenomenon */
CREATE TABLE `Phenomenon` (
  `PhenomenonID` INT NOT NULL AUTO_INCREMENT,
  `Phenomenon` VARCHAR(3),
  PRIMARY KEY (`PhenomenonID`)
)

/* ->>---<<- */
CREATE TABLE `WeatherPhenomenon` (
  `WeatherID` INT NOT NULL,
  `PhenomenonID` INT NOT NULL,
  FOREIGN KEY (`WeatherID`) REFERENCES `Weather`(`WeatherID`),
  FOREIGN KEY (`PhenomenonID`) REFERENCES `Phenomenon`(`PhenomenonID`)
)

/* Group -||---O|- WindShear */
CREATE TABLE `WindShear` (
  `GroupID` INT NOT NULL AUTO_INCREMENT,
  `Altitude` INT,
  `Direction` INT,
  `Speed` INT,
  `Unit` VARCHAR(4),
  PRIMARY KEY (`GroupID`),
  FOREIGN KEY (`GroupID`) REFERENCES `Group`(`GroupID`)
)