SELECT `TAF`.`ICAOCode` AS `ICAO`,
       `TAF`.`OriginDateTime` AS `Time`,
       `TAF`.`ValidFromDateTime` AS `TAFFrom`,
       `TAF`.`ValidTillDateTime` AS `TAFTill`,
       `GroupHeader`.`FromDateTime` AS `GroupFrom`,
       `GroupHeader`.`TillDateTime` AS `GroupTill`,
       `Wind`.`Direction` AS `WindDirection`,
       `Wind`.`Speed` AS `WindSpeed`,
       `Wind`.`Gust` AS `WindGust`,
       `Visibility`.`MoreThan` AS `VisibilityMoreThan`,
       `Visibility`.`Range` AS `VisibilityRange`,
       `Cloud`.`Layer` AS `CloudLayer`,
       `Cloud`.`Ceiling` AS `CloudCeiling`,
       `Cloud`.`Type` AS `CloudType`,
       `VerticalVisibility`.`VerticalVisibility`,
       `Intensity`.`Intensity` AS `WeatherIntensity`,
       `Modifier`.`Modifier` AS `WeatherModifier`,
       `Phenomenon`.`Phenomenon` AS `WeatherPhenomenon`,
       `WindShear`.`Altitude` AS `WindShearAltitude`,
       `WindShear`.`Direction` AS `WindShearDirection`,
       `WindShear`.`Speed` AS `WindShearSpeed`
FROM `TAF`
LEFT JOIN `Group`
  ON `TAF`.`TAFID` = `Group`.`GroupID`
LEFT JOIN `GroupHeader`
  ON `Group`.`GroupID` = `GroupHeader`.`GroupID`
LEFT JOIN `Wind`
  ON `Group`.`GroupID` = `Wind`.`GroupID`
LEFT JOIN `Visibility`
  ON `Group`.`GroupID` = `Visibility`.`GroupID`
LEFT JOIN `Cloud`
  ON `Group`.`GroupID` = `Cloud`.`GroupID`
LEFT JOIN `VerticalVisibility`
  ON `Group`.`GroupID` = `VerticalVisibility`.`GroupID`
LEFT JOIN `Weather`
  ON `Group`.`GroupID` = `Weather`.`GroupID`
LEFT JOIN `WeatherIntensity`
  ON `Weather`.`WeatherID` = `WeatherIntensity`.`WeatherID`
LEFT JOIN `Intensity`
  ON `WeatherIntensity`.`IntensityID` = `Intensity`.`IntensityID`
LEFT JOIN `WeatherModifier`
  ON `Weather`.`WeatherID` = `WeatherModifier`.`WeatherID`
LEFT JOIN `Modifier`
  ON `WeatherModifier`.`ModifierID` = `Modifier`.`ModifierID`
LEFT JOIN `WeatherPhenomenon`
  ON `Weather`.`WeatherID` = `WeatherPhenomenon`.`WeatherID`
LEFT JOIN `Phenomenon`
  ON `WeatherPhenomenon`.`PhenomenonID` = `Phenomenon`.`PhenomenonID`
LEFT JOIN `WindShear`
  ON `Group`.`GroupID` = `WindShear`.`GroupID`
WHERE `TAF`.`ICAOCode` = 'KORD'
ORDER BY `TAF`.`ValidFromDateTime` ASC