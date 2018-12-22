USE `Schedule`;

SELECT `Flight`.`ICAONumber` AS `FlightNumber`,
       `Schedule`.`Status` AS `Status`,
       `Departure`.`ICAOCode` AS `Departure`,
       `Arrival`.`ICAOCode` AS `Arrival`,
       `Departure`.`ScheduledTime` AS `ScheduledDeparture`,
       `Arrival`.`ScheduledTime` AS `ScheduledArrival`,
       `Departure`.`ActualTime` AS `ActualDeparture`,
       `Arrival`.`ActualTime` AS `ActualArrival`
FROM `Schedule`
INNER JOIN `Flight`
  ON `Schedule`.`FlightID` = `Flight`.`FlightID`
INNER JOIN `Departure`
  ON `Schedule`.`ScheduleID` = `Departure`.`ScheduleID`
INNER JOIN `Arrival`
  ON `Schedule`.`ScheduleID` = `Arrival`.`ScheduleID`
WHERE `Schedule`.`Type` = 'departure'
ORDER BY `Departure`.`ScheduledTime` ASC