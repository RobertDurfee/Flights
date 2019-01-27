USE `Schedule`;

SELECT DISTINCT `Arrival`.`ICAOCode`,
  COUNT(*) AS `FlightsFrom`
FROM `Schedule`
INNER JOIN `Flight`
  ON `Schedule`.`FlightID` = `Flight`.`FlightID`
INNER JOIN `Arrival`
  ON `Schedule`.`ScheduleID` = `Arrival`.`ScheduleID`
WHERE `Schedule`.`Type` = 'departure'
  AND `Arrival`.`ICAOCode` LIKE 'K%'
GROUP BY `Arrival`.`ICAOCode`
ORDER BY `FlightsFrom` DESC
