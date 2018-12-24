USE `METAR`;

SELECT *
FROM `METAR` as mt
LEFT JOIN `RunwayVisibility` AS rv
  ON mt.`METARID` = rv.`METARID`
LEFT JOIN `PresentWeather` AS pw
  ON mt.`METARID` = pw.`METARID`
LEFT JOIN `RecentWeather` AS rw
  ON mt.`METARID` = rw.`METARID`
LEFT JOIN `SkyCondition` AS sc
  ON mt.`METARID` = sc.`METARID`
LEFT JOIN `WindShearRunway` AS ws
  ON mt.`METARID` = ws.`METARID`
LEFT JOIN `Remark` AS rm
  ON mt.`METARID` = rm.`METARID`;