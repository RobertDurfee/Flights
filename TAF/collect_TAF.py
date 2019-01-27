import requests
from bs4 import BeautifulSoup
import mysql.connector
import pytaf
from datetime import datetime
import re


def replace_line_breaks(soup):

  for br in soup.find_all('br'):
    br.replace_with('\n')
  
  return soup


def fetch(icao_code):

  response = requests.get('https://www.aviationweather.gov/taf/board?ids=' + icao_code + '&date=&submit=Goto+TAF+board')
  soup = BeautifulSoup(response.text, 'html.parser')

  taf_soup = soup.select('#awc_main_content_wrap > code')[0]
  taf_soup = replace_line_breaks(taf_soup)

  return taf_soup.get_text()


def get_intensity_id(cxn, intensity):

  cursor = cxn.cursor()

  query = '''
    SELECT `Intensity`.`IntensityID`
    FROM `Intensity`
    WHERE `Intensity`.`Intensity` = %(intensity)s
    '''
  
  cursor.execute(query, { 'intensity': intensity })
  rows = cursor.fetchall()

  cursor.close()

  return rows[0][0] if len(rows) > 0 else None


def get_modifier_id(cxn, modifier):

  cursor = cxn.cursor()

  query = '''
    SELECT `Modifier`.`ModifierID`
    FROM `Modifier`
    WHERE `Modifier`.`Modifier` = %(modifier)s
    '''
  
  cursor.execute(query, { 'modifier': modifier })
  rows = cursor.fetchall()

  cursor.close()

  return rows[0][0] if len(rows) > 0 else None


def get_phenomenon_id(cxn, phenomenon):

  cursor = cxn.cursor()

  query = '''
    SELECT `Phenomenon`.`PhenomenonID`
    FROM `Phenomenon`
    WHERE `Phenomenon`.`Phenomenon` = %(phenomenon)s
    '''
  
  cursor.execute(query, { 'phenomenon': phenomenon })
  rows = cursor.fetchall()

  cursor.close()

  return rows[0][0] if len(rows) > 0 else None


def insert_taf(cxn, taf):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `TAF` (
      `Type`,
      `ICAOCode`,
      `OriginDateTime`,
      `ValidFromDateTime`,
      `ValidTillDateTime`,
      `Form`,
      `Code`
    ) VALUES (
      %(type)s,
      %(icao_code)s,
      %(origin_date_time)s,
      %(valid_from_date_time)s,
      %(valid_till_date_time)s,
      %(form)s,
      %(code)s
    )
    '''

  cursor.execute(query, taf)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_group(cxn, group):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Group` (
      `TAFID`,
      `Code`
    ) VALUES (
      %(taf_id)s,
      %(code)s
    )
    '''
  
  cursor.execute(query, group)
  id = cursor.lastrowid
  
  cxn.commit()
  cursor.close()

  return id


def insert_group_header(cxn, group_header):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `GroupHeader` (
      `GroupID`,
      `Type`,
      `Probability`,
      `FromDateTime`,
      `TillDateTime`
    ) VALUES (
      %(group_id)s,
      %(type)s,
      %(probability)s,
      %(from_date_time)s,
      %(till_date_time)s
    )
    '''
  
  cursor.execute(query, group_header)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_wind(cxn, wind):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Wind` (
      `GroupID`,
      `Direction`,
      `Speed`,
      `Gust`,
      `Unit`
    ) VALUES (
      %(group_id)s,
      %(direction)s,
      %(speed)s,
      %(gust)s,
      %(unit)s
    )
    '''
  
  cursor.execute(query, wind)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_visibility(cxn, visibility):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Visibility` (
      `GroupID`,
      `MoreThan`,
      `Range`,
      `Unit`
    ) VALUES (
      %(group_id)s,
      %(more_than)s,
      %(range)s,
      %(unit)s
    )
    '''
  
  cursor.execute(query, visibility)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_cloud(cxn, cloud):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Cloud` (
      `GroupID`,
      `Layer`,
      `Ceiling`,
      `Type`
    ) VALUES (
      %(group_id)s,
      %(layer)s,
      %(ceiling)s,
      %(type)s
    )
    '''
  
  cursor.execute(query, cloud)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_vertical_visibility(cxn, vertical_visibility):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `VerticalVisibility` (
      `GroupID`,
      `VerticalVisibility`
    ) VALUES (
      %(group_id)s,
      %(vertical_visibility)s
    )
    '''
  
  cursor.execute(query, vertical_visibility)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_weather(cxn, weather):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Weather` (
      `GroupID`
    ) VALUES (
      %(group_id)s
    )
    '''
  
  cursor.execute(query, weather)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_intensity(cxn, intensity):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Intensity` (
      `Intensity`
    ) VALUES (
      %(intensity)s
    )
    '''
  
  cursor.execute(query, intensity)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_weather_intensity(cxn, weather_intensity):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `WeatherIntensity` (
      `WeatherID`,
      `IntensityID`
    ) VALUES (
      %(weather_id)s,
      %(intensity_id)s
    )
    '''
  
  cursor.execute(query, weather_intensity)

  cxn.commit()
  cursor.close()


def insert_modifier(cxn, modifier):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Modifier` (
      `Modifier`
    ) VALUES (
      %(modifier)s
    )
    '''
  
  cursor.execute(query, modifier)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_weather_modifier(cxn, weather_modifier):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `WeatherModifier` (
      `WeatherID`,
      `ModifierID`
    ) VALUES (
      %(weather_id)s,
      %(modifier_id)s
    )
    '''
  
  cursor.execute(query, weather_modifier)

  cxn.commit()
  cursor.close()


def insert_phenomenon(cxn, phenomenon):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Phenomenon` (
      `Phenomenon`
    ) VALUES (
      %(phenomenon)s
    )
    '''
  
  cursor.execute(query, phenomenon)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_weather_phenomenon(cxn, weather_phenomenon):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `WeatherPhenomenon` (
      `WeatherID`,
      `PhenomenonID`
    ) VALUES (
      %(weather_id)s,
      %(phenomenon_id)s
    )
    '''
  
  cursor.execute(query, weather_phenomenon)

  cxn.commit()
  cursor.close()


def insert_wind_shear(cxn, wind_shear):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `WindShear` (
      `GroupID`,
      `Altitude`,
      `Direction`,
      `Speed`,
      `Unit`
    ) VALUES (
      %(group_id)s,
      %(altitude)s,
      %(direction)s,
      %(speed)s,
      %(unit)s
    )
    '''
  
  cursor.execute(query, wind_shear)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def construct_date_time(date, hours, minutes=None):
  """ Year and month need to be inferred """

  date_match = re.match(r'\d{1,2}', date) if date else None
  hours_match = re.match(r'\d{1,2}', hours) if hours else None
  minutes_match = re.match(r'\d{1,2}', minutes) if minutes else None

  # If date or hours cannot be constructed, return
  if not date_match or not hours_match:
    return None
  
  date = int(date_match.group(0))
  hours = int(hours_match.group(0))

  # If minutes cannot be constructed, default to 0
  if minutes_match:
    minutes = int(minutes_match.group(0))
  else:
    minutes = 0

  now = datetime.now()

  # If date occurred in previous month
  if date - now.day >= 27:
    month = now.month - 1
  # If date occured in next month
  elif date - now.day <= -27:
    month = now.month + 1
  # If date occured in same month
  else:
    month = now.month

  # Ensure within [1..12]
  month = (month - 1) % 12 + 1

  # If month occurred in previous year
  if month - now.month == 11:
    year = now.year - 1
  # If month occurred in next year
  elif month - now.month == -11:
    year = now.year + 1
  # If month occurred in same year
  else:
    year = now.year

  # Sometimes the hours are reported as '24'
  days_in_month = [ None, 31, 28 + (1 if year % 4 == 0 else 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

  if hours == 24:
    hours = 0
    if date != days_in_month[month]:
      date += 1
    # If last day in month, advance month, set first
    else:
      date = 1
      if month != 12:
        month += 1
      # If December, advance year, set January
      else:
        month = 1
        year += 1

  return datetime(year, month, date, hours, minutes)


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

      cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='TAF')

      raw_taf = fetch(airport)
      parsed_taf = pytaf.TAF(raw_taf)

      taf = {
        'type': parsed_taf._taf_header.get('type'),
        'icao_code': parsed_taf._taf_header.get('icao_code'),
        'origin_date_time': construct_date_time(parsed_taf._taf_header.get('origin_date'), parsed_taf._taf_header.get('origin_hours'), parsed_taf._taf_header.get('origin_minutes')),
        'valid_from_date_time': construct_date_time(parsed_taf._taf_header.get('valid_from_date'), parsed_taf._taf_header.get('valid_from_hours')),
        'valid_till_date_time': construct_date_time(parsed_taf._taf_header.get('valid_till_date'), parsed_taf._taf_header.get('valid_till_hours')),
        'form': parsed_taf._taf_header.get('form'),
        'code': parsed_taf._raw_taf
      }

      taf_id = insert_taf(cxn, taf)

      for (parsed_group, raw_group) in zip(parsed_taf._weather_groups, parsed_taf._raw_weather_groups):

        group = {
          'taf_id': taf_id,
          'code': raw_group
        }

        group_id = insert_group(cxn, group)

        parsed_group_header = parsed_group.get('header')
        if parsed_group_header and len(parsed_group_header) > 0:

          group_header = {
            'group_id': group_id,
            'type': parsed_group_header.get('type'),
            'probability': int(parsed_group_header.get('probability')) if parsed_group_header.get('probability') is not None else None,
            'from_date_time': construct_date_time(parsed_group_header.get('from_date'), parsed_group_header.get('from_hours')),
            'till_date_time': construct_date_time(parsed_group_header.get('till_date'), parsed_group_header.get('till_hours'))
          }

          insert_group_header(cxn, group_header)
        
        parsed_wind = parsed_group.get('wind')
        if parsed_wind and len(parsed_wind) > 0:

          wind = {
            'group_id': group_id,
            'direction': parsed_wind.get('direction'),
            'speed': int(parsed_wind.get('speed')) if parsed_wind.get('speed') is not None else None,
            'gust': int(parsed_wind.get('gust')) if parsed_wind.get('gust') is not None else None,
            'unit': parsed_wind.get('unit')
          }

          insert_wind(cxn, wind)
        
        parsed_visibility = parsed_group.get('visibility')
        if parsed_visibility and len(parsed_visibility) > 0:

          visibility = {
            'group_id': group_id,
            'more_than': parsed_visibility.get('more') == 'P',
            'range': parsed_visibility.get('range'),
            'unit': parsed_visibility.get('unit')
          }

          insert_visibility(cxn, visibility)
        
        for parsed_cloud in parsed_group.get('clouds', []):

          cloud = {
            'group_id': group_id,
            'layer': parsed_cloud.get('layer'),
            'ceiling': int(parsed_cloud.get('ceiling')) if parsed_cloud.get('ceiling') is not None else None,
            'type': parsed_cloud.get('type')
          }

          insert_cloud(cxn, cloud)
        
        parsed_vertical_visibility = parsed_group.get('vertical_visibility')
        if parsed_vertical_visibility:

          vertical_visibility = {
            'group_id': group_id,
            'vertical_visibility': parsed_vertical_visibility
          }

          insert_vertical_visibility(cxn, vertical_visibility)

        for parsed_weather in parsed_group.get('weather', []):

          weather = {
            'group_id': group_id
          }

          weather_id = insert_weather(cxn, weather)

          for parsed_intensity in parsed_weather.get('intensity', []):

            intensity_id = get_intensity_id(cxn, parsed_intensity)
            if intensity_id is None:
              intensity_id = insert_intensity(cxn, { 'intensity': parsed_intensity }) 
            
            weather_intensity = {
              'weather_id': weather_id,
              'intensity_id': intensity_id
            }

            insert_weather_intensity(cxn, weather_intensity)
          
          for parsed_modifier in parsed_weather.get('modifier', []):

            modifier_id = get_modifier_id(cxn, parsed_modifier)
            if modifier_id is None:
              modifier_id = insert_modifier(cxn, { 'modifier': parsed_modifier })
            
            weather_modifier = {
              'weather_id': weather_id,
              'modifier_id': modifier_id
            }

            insert_weather_modifier(cxn, weather_modifier)
          
          for parsed_phenomenon in parsed_weather.get('phenomenon', []):

            phenomenon_id = get_phenomenon_id(cxn, parsed_phenomenon)
            if phenomenon_id is None:
              phenomenon_id = insert_phenomenon(cxn, { 'phenomenon': parsed_phenomenon })
            
            weather_phenomenon = {
              'weather_id': weather_id,
              'phenomenon_id': phenomenon_id
            }

            insert_weather_phenomenon(cxn, weather_phenomenon)
        
        parsed_wind_shear = parsed_group.get('windshear')
        if parsed_wind_shear and len(parsed_wind_shear) > 0:

          wind_shear = {
            'group_id': group_id,
            'altitude': int(parsed_wind_shear.get('altitude')) if parsed_wind_shear.get('altitude') is not None else None,
            'direction': int(parsed_wind_shear.get('direction')) if parsed_wind_shear.get('direction') is not None else None,
            'speed': int(parsed_wind_shear.get('speed')) if parsed_wind_shear.get('speed') is not None else None,
            'unit': parsed_wind_shear.get('unit')
          }

          insert_wind_shear(cxn, wind_shear)

    except:
      print(airport + ' failed.')

    finally:
      if 'cxn' in locals() or 'cxn' in globals(): cxn.close()
