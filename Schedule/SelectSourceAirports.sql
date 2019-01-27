USE `Schedule`;

SELECT DISTINCT `Departure`.`ICAOCode`,
  COUNT(*) AS `FlightsFrom`
FROM `Schedule`
INNER JOIN `Flight`
  ON `Schedule`.`FlightID` = `Flight`.`FlightID`
INNER JOIN `Departure`
  ON `Schedule`.`ScheduleID` = `Departure`.`ScheduleID`
WHERE `Schedule`.`Type` = 'arrival'
  AND `Departure`.`ICAOCode` LIKE 'K%'
GROUP BY `Departure`.`ICAOCode`
ORDER BY `FlightsFrom` DESC
