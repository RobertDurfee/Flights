import requests
from metar import Metar
import mysql.connector


def insert_metar(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `METAR` (
      `Type`, 
      `Mode`, 
      `StationID`, 
      `Time`, 
      `Cycle`, 
      `WindDirection`, 
      `WindSpeed`, 
      `WindGust`, 
      `WindDirectionFrom`, 
      `WindDirectionTo`, 
      `Visibility`, 
      `VisibilityDirection`, 
      `MaxVisibility`, 
      `MaxVisibilityDirection`, 
      `Temperature`, 
      `DewPoint`, 
      `Pressure`, 
      `SeaLevelPressure`, 
      `PeakWindSpeed`, 
      `PeakWindDirection`, 
      `MaxTemperature6Hr`, 
      `MinTemperature6Hr`, 
      `MaxTemperature24Hr`, 
      `MinTemperature24Hr`, 
      `Precipitation1Hr`, 
      `Precipitation3Hr`, 
      `Precipitation6Hr`, 
      `Precipitation24Hr`,
      `Code`
    ) VALUES (
      %(Type)s, 
      %(Mode)s, 
      %(StationID)s, 
      %(Time)s, 
      %(Cycle)s, 
      %(WindDirection)s, 
      %(WindSpeed)s, 
      %(WindGust)s, 
      %(WindDirectionFrom)s, 
      %(WindDirectionTo)s, 
      %(Visibility)s, 
      %(VisibilityDirection)s, 
      %(MaxVisibility)s, 
      %(MaxVisibilityDirection)s, 
      %(Temperature)s, 
      %(DewPoint)s, 
      %(Pressure)s, 
      %(SeaLevelPressure)s, 
      %(PeakWindSpeed)s, 
      %(PeakWindDirection)s, 
      %(MaxTemperature6Hr)s, 
      %(MinTemperature6Hr)s, 
      %(MaxTemperature24Hr)s, 
      %(MinTemperature24Hr)s, 
      %(Precipitation1Hr)s, 
      %(Precipitation3Hr)s, 
      %(Precipitation6Hr)s, 
      %(Precipitation24Hr)s,
      %(Code)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_runway_visibility(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `RunwayVisibility` (
      `METARID`,
      `Name`,
      `Low`,
      `High`
    ) VALUES (
      %(METARID)s,
      %(Name)s,
      %(Low)s,
      %(High)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_present_weather(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `PresentWeather` (
      `METARID`,
      `Intensity`,
      `Descriptor`,
      `Precipitation`,
      `Obscuration`,
      `Other`
    ) VALUES (
      %(METARID)s,
      %(Intensity)s,
      %(Descriptor)s,
      %(Precipitation)s,
      %(Obscuration)s,
      %(Other)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_recent_weather(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `RecentWeather` (
      `METARID`,
      `Intensity`,
      `Descriptor`,
      `Precipitation`,
      `Obscuration`,
      `Other`
    ) VALUES (
      %(METARID)s,
      %(Intensity)s,
      %(Descriptor)s,
      %(Precipitation)s,
      %(Obscuration)s,
      %(Other)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_sky_condition(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `SkyCondition` (
      `METARID`,
      `Cover`,
      `Height`,
      `Cloud`
    ) VALUES (
      %(METARID)s,
      %(Cover)s,
      %(Height)s,
      %(Cloud)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_wind_shear_runway(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `WindShearRunway` (
      `METARID`,
      `Runway`
    ) VALUES (
      %(METARID)s,
      %(Runway)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_remark(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Remark` (
      `METARID`,
      `Remark`
    ) VALUES (
      %(METARID)s,
      %(Remark)s
    )
    '''

  cursor.execute(query, data)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def fetch(icao_code):

  response = requests.get('http://tgftp.nws.noaa.gov/data/observations/metar/stations/' + icao_code + '.TXT')
  raw_metar = response.text.split('\n')[1]

  return raw_metar


if __name__ == '__main__':

  airports = [
    'KORD', 'KSTL', 'KSFO', 'KCAK', 'KRDU', 'KBDL', 'KLNK', 'KMDT', 'KJFK', 'KSEA', 'KCHO',
    'KRSW', 'KAUS', 'KGRR', 'KFLL', 'KPSP', 'KATW', 'KCVG', 'KFNT', 'KCMI', 'KBTV', 'KDAY',
    'KBHM', 'KSMF', 'KGSO', 'KCAE', 'KCLE', 'KAZO', 'KLAS', 'KBNA', 'KTYS', 'KSUX', 'KUNV',
    'KICT', 'KGRB', 'KLGA', 'KDBQ', 'KAVL', 'KRIC', 'KOKC', 'KPIA', 'KMSP', 'KSAV', 'KPHL',
    'KABQ', 'KCOS', 'KDFW', 'KBUF', 'KMCO', 'KALB', 'KAVP', 'KCHA', 'KEAU', 'KDCA', 'KALO',
    'KCLT', 'KBIS', 'KMKE', 'KJAN', 'KMLI', 'KXNA', 'KMSY', 'KTUL', 'KBOI', 'KLAX', 'KIAD',
    'KIAH', 'KDEN', 'KMBS', 'KRST', 'KJAX', 'KPBI', 'KSNA', 'KFAR', 'KELP', 'KCHS', 'KCWA',
    'KFWA', 'KSBN', 'KSAT', 'KCMH', 'KIND', 'KCID', 'KBMI', 'KMIA', 'KBWI', 'KPIT', 'KCMX',
    'KLAN', 'KGSP', 'KLSE', 'KSGF', 'KTOL', 'KOMA', 'KTPA', 'KPWM', 'KTVC', 'KHPN', 'KDLH',
    'KSAN', 'KSRQ', 'KEWR', 'KROC', 'KPDX', 'KORF', 'KMKG', 'KSPI', 'KMSN', 'KATL', 'KCOU',
    'KDSM', 'KILM', 'KROA', 'KMEM', 'KHSV', 'KSLC', 'KLEX', 'KSDF', 'KEVV', 'KFSD', 'KDTW',
    'KBOS', 'KSYR', 'KASE', 'KPHX', 'KMCI', 'KLIT'
  ]

  for airport in airports:

    try:

      cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='METAR')

      raw_metar = fetch(airport)
      parsed_metar = Metar.Metar(raw_metar)

      metar_data = {
        'Type': parsed_metar.type,
        'Mode': parsed_metar.mod,
        'StationID': parsed_metar.station_id,
        'Time': parsed_metar.time,
        'Cycle': parsed_metar.cycle,
        'WindDirection': parsed_metar.wind_dir.value() if parsed_metar.wind_dir else None,
        'WindSpeed': parsed_metar.wind_speed.value('KT') if parsed_metar.wind_speed else None,
        'WindGust': parsed_metar.wind_gust.value('KT') if parsed_metar.wind_gust else None,
        'WindDirectionFrom': parsed_metar.wind_dir_from.value() if parsed_metar.wind_dir_from else None,
        'WindDirectionTo': parsed_metar.wind_dir_to.value() if parsed_metar.wind_dir_to else None,
        'Visibility': parsed_metar.vis.value('SM') if parsed_metar.vis else None,
        'VisibilityDirection': parsed_metar.vis_dir.value() if parsed_metar.vis_dir else None,
        'MaxVisibility': parsed_metar.max_vis.value('SM') if parsed_metar.max_vis else None,
        'MaxVisibilityDirection': parsed_metar.max_vis_dir.value() if parsed_metar.max_vis_dir else None,
        'Temperature': parsed_metar.temp.value('C') if parsed_metar.temp else None,
        'DewPoint': parsed_metar.dewpt.value('C') if parsed_metar.dewpt else None,
        'Pressure': parsed_metar.press.value('IN') if parsed_metar.press else None,
        'SeaLevelPressure': parsed_metar.press_sea_level.value('MB') if parsed_metar.press_sea_level else None,
        'PeakWindSpeed': parsed_metar.wind_speed_peak.value('KT') if parsed_metar.wind_speed_peak else None,
        'PeakWindDirection': parsed_metar.wind_dir_peak.value() if parsed_metar.wind_dir_peak else None,
        'MaxTemperature6Hr': parsed_metar.max_temp_6hr.value('C') if parsed_metar.max_temp_6hr else None,
        'MinTemperature6Hr': parsed_metar.min_temp_6hr.value('C') if parsed_metar.min_temp_6hr else None,
        'MaxTemperature24Hr': parsed_metar.max_temp_24hr.value('C') if parsed_metar.max_temp_24hr else None,
        'MinTemperature24Hr': parsed_metar.min_temp_24hr.value('C') if parsed_metar.min_temp_24hr else None,
        'Precipitation1Hr': parsed_metar.precip_1hr.value('CM') if parsed_metar.precip_1hr else None,
        'Precipitation3Hr': parsed_metar.precip_3hr.value('CM') if parsed_metar.precip_3hr else None,
        'Precipitation6Hr': parsed_metar.precip_6hr.value('CM') if parsed_metar.precip_6hr else None,
        'Precipitation24Hr': parsed_metar.precip_24hr.value('CM') if parsed_metar.precip_24hr else None,
        'Code': parsed_metar.code
      }

      metar_id = insert_metar(cxn, metar_data)

      for (name, low, high, _) in parsed_metar.runway:

        runway_visibility_data = {
          'METARID': metar_id,
          'Name': name,
          'Low': low.value('SM') if low else None,
          'High': high.value('SM') if high else None
        }

        insert_runway_visibility(cxn, runway_visibility_data)

      for (intensity, descriptor, precipitation, obscuration, other) in parsed_metar.weather:

        present_weather_data = {
          'METARID': metar_id,
          'Intensity': intensity,
          'Descriptor': descriptor,
          'Precipitation': precipitation,
          'Obscuration': obscuration,
          'Other': other
        }

        insert_present_weather(cxn, present_weather_data)
      
      for (intensity, descriptor, precipitation, obscuration, other) in parsed_metar.recent:

        recent_weather_data = {
          'METARID': metar_id,
          'Intensity': intensity,
          'Descriptor': descriptor,
          'Precipitation': precipitation,
          'Obscuration': obscuration,
          'Other': other
        }

        insert_recent_weather(cxn, recent_weather_data)
      
      for (cover, height, cloud) in parsed_metar.sky:

        sky_condition_data = {
          'METARID': metar_id,
          'Cover': cover,
          'Height': height.value('FT') if height else None,
          'Cloud': cloud
        }

        insert_sky_condition(cxn, sky_condition_data)

      for runway in parsed_metar.windshear:

        wind_shear_runway_data = {
          'METARID': metar_id,
          'Runway': runway
        }

        insert_wind_shear_runway(cxn, wind_shear_runway_data)
      
      for remark in parsed_metar._remarks:
      
        remark_data = {
          'METARID': metar_id,
          'Remark': remark
        }

        insert_remark(cxn, remark_data)

    except:
      print(airport + ' failed.')

    finally:
      if 'cxn' in locals() or 'cxn' in globals(): cxn.close()
