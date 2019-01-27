import requests
import mysql.connector
import os
import json
import objectpath


def get_key():

  key_file = open(os.environ['AVIATION_EDGE_API_KEY'], 'r')
  key = key_file.read().split('\n')[0]
  key_file.close()

  return key


def fetch(icao_code, type):

  response = requests.get('https://aviation-edge.com/v2/public/timetable?key=' + get_key() + '&icaoCode=' + icao_code + '&type=' + type)

  return json.loads(response.text)


def schedule_exists(cxn, schedule):

  cursor = cxn.cursor()

  query = '''
    SELECT `Schedule`.`ScheduleID`
    FROM `Schedule`
    INNER JOIN `Departure`
      ON `Schedule`.`ScheduleID` = `Departure`.`ScheduleID`
    INNER JOIN `Arrival`
      ON `Schedule`.`ScheduleID` = `Arrival`.`ScheduleID`
    INNER JOIN `Flight`
      ON `Schedule`.`FlightID` = `Flight`.`FlightID`
    WHERE `Departure`.`ICAOCode` = %(departure_icao)s
      AND `Departure`.`ScheduledTime` = %(scheduled_departure)s
      AND `Arrival`.`ICAOCode` = %(arrival_icao)s
      AND `Arrival`.`ScheduledTime` = %(scheduled_arrival)s
      AND `Flight`.`ICAONumber` = %(flight_icao)s
    '''
  
  cursor.execute(query, schedule)
  rows = cursor.fetchall()

  cursor.close()

  return (len(rows) >= 1)


def get_airline_id(cxn, icao_code):

  cursor = cxn.cursor()

  query = '''
    SELECT `Airline`.`AirlineID`
    FROM `Airline`
    WHERE `Airline`.`ICAOCode` = %(icao_code)s
    '''

  cursor.execute(query, { 'icao_code': icao_code })
  rows = cursor.fetchall()

  cursor.close()

  return rows[0][0] if len(rows) > 0 else None


def get_flight_id(cxn, icao_number):

  cursor = cxn.cursor()

  query = '''
    SELECT `Flight`.`FlightID`
    FROM `Flight`
    WHERE `Flight`.`ICAONumber` = %(icao_number)s
    '''
  
  cursor.execute(query, { 'icao_number': icao_number })
  rows = cursor.fetchall()

  cursor.close()

  return rows[0][0] if len(rows) > 0 else None


def insert_schedule(cxn, schedule):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Schedule` (
      `Type`,
      `Status`,
      `AirlineID`,
      `FlightID`
    ) VALUES (
      %(type)s,
      %(status)s,
      %(airline_id)s,
      %(flight_id)s
    )
    '''
  
  cursor.execute(query, schedule)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_departure(cxn, departure):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Departure` (
      `ScheduleID`,
      `ICAOCode`,
      `IATACode`,
      `Terminal`,
      `Gate`,
      `Delay`,
      `ScheduledTime`,
      `EstimatedTime`,
      `ActualTime`,
      `EstimatedRunway`,
      `ActualRunway`
    ) VALUES (
      %(schedule_id)s,
      %(icao_code)s,
      %(iata_code)s,
      %(terminal)s,
      %(gate)s,
      %(delay)s,
      %(scheduled_time)s,
      %(estimated_time)s,
      %(actual_time)s,
      %(estimated_runway)s,
      %(actual_runway)s
    )
    '''
  
  cursor.execute(query, departure)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_arrival(cxn, arrival):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Arrival` (
      `ScheduleID`,
      `ICAOCode`,
      `IATACode`,
      `Terminal`,
      `Gate`,
      `Baggage`,
      `Delay`,
      `ScheduledTime`,
      `EstimatedTime`,
      `ActualTime`,
      `EstimatedRunway`,
      `ActualRunway`
    ) VALUES (
      %(schedule_id)s,
      %(icao_code)s,
      %(iata_code)s,
      %(terminal)s,
      %(gate)s,
      %(baggage)s,
      %(delay)s,
      %(scheduled_time)s,
      %(estimated_time)s,
      %(actual_time)s,
      %(estimated_runway)s,
      %(actual_runway)s
    )
    '''
  
  cursor.execute(query, arrival)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_airline(cxn, airline):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Airline` (
      `Name`,
      `ICAOCode`,
      `IATACode`
    ) VALUES (
      %(name)s,
      %(icao_code)s,
      %(iata_code)s
    )
    '''
  
  cursor.execute(query, airline)
  id = cursor.lastrowid

  cxn.commit()
  cursor.close()

  return id


def insert_flight(cxn, flight):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Flight` (
      `Number`,
      `ICAONumber`,
      `IATANumber`
    ) VALUES (
      %(number)s,
      %(icao_number)s,
      %(iata_number)s
    )
    '''
  
  cursor.execute(query, flight)
  id = cursor.lastrowid
  
  cxn.commit()
  cursor.close()

  return id


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

      cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='Schedule')

      departures = fetch(airport, 'departure')
      departures_tree = objectpath.Tree(departures)
      completed_departures = list(departures_tree.execute("$.*[@.arrival.actualTime or @.status is 'cancelled']"))

      arrivals = fetch(airport, 'arrival')
      arrivals_tree = objectpath.Tree(arrivals)
      completed_arrivals = list(arrivals_tree.execute("$.*[@.arrival.actualTime or @.status is 'cancelled']"))

      new_departures = 0
      new_arrivals = 0

      for completed in (completed_departures + completed_arrivals):

        schedule = {
          'departure_icao': completed.get('departure', {}).get('icaoCode'),
          'scheduled_departure': completed.get('departure', {}).get('scheduledTime'),
          'arrival_icao': completed.get('arrival', {}).get('icaoCode'),
          'scheduled_arrival': completed.get('arrival', {}).get('scheduledTime'),
          'flight_icao': completed.get('flight', {}).get('icaoNumber')
        }

        if not schedule_exists(cxn, schedule):

          if completed.get('type') == 'departure':
            new_departures += 1
          elif completed.get('type') == 'arrival':
            new_arrivals += 1
          
          airline_id = get_airline_id(cxn, completed.get('airline', {}).get('icaoCode'))

          if airline_id is None:

            airline = {
              'name': completed.get('airline', {}).get('name'),
              'icao_code': completed.get('airline', {}).get('icaoCode'),
              'iata_code': completed.get('airline', {}).get('iataCode')
            }

            airline_id = insert_airline(cxn, airline)
          
          flight_id = get_flight_id(cxn, completed.get('flight', {}).get('icaoNumber'))

          if flight_id is None:

            flight = {
              'number': completed.get('flight', {}).get('number'),
              'icao_number': completed.get('flight', {}).get('icaoNumber'),
              'iata_number': completed.get('flight', {}).get('iataNumber')
            }

            flight_id = insert_flight(cxn, flight)
          
          schedule = {
            'type': completed.get('type'),
            'status': completed.get('status'),
            'airline_id': airline_id,
            'flight_id': flight_id
          }
          
          schedule_id = insert_schedule(cxn, schedule)

          departure = {
            'schedule_id': schedule_id,
            'icao_code': completed.get('departure', {}).get('icaoCode'),
            'iata_code': completed.get('departure', {}).get('iataCode'),
            'terminal': completed.get('departure', {}).get('terminal'),
            'gate': completed.get('departure', {}).get('gate'),
            'delay': completed.get('departure', {}).get('delay'),
            'scheduled_time': completed.get('departure', {}).get('scheduledTime'),
            'estimated_time': completed.get('departure', {}).get('estimatedTime'),
            'actual_time': completed.get('departure', {}).get('actualTime'),
            'estimated_runway': completed.get('departure', {}).get('estimatedRunway'),
            'actual_runway': completed.get('departure', {}).get('actualRunway')
          }

          insert_departure(cxn, departure)

          arrival = {
            'schedule_id': schedule_id,
            'icao_code': completed.get('arrival', {}).get('icaoCode'),
            'iata_code': completed.get('arrival', {}).get('iataCode'),
            'terminal': completed.get('arrival', {}).get('terminal'),
            'gate': completed.get('arrival', {}).get('gate'),
            'baggage': completed.get('arrival', {}).get('baggage'),
            'delay': completed.get('arrival', {}).get('delay'),
            'scheduled_time': completed.get('arrival', {}).get('scheduledTime'),
            'estimated_time': completed.get('arrival', {}).get('estimatedTime'),
            'actual_time': completed.get('arrival', {}).get('actualTime'),
            'estimated_runway': completed.get('arrival', {}).get('estimatedRunway'),
            'actual_runway': completed.get('arrival', {}).get('actualRunway')
          }

          insert_arrival(cxn, arrival)

      print(' D:' + str(new_departures) + '/' + str(len(completed_departures)) + '/' + str(len(departures)), end='')
      print(' A:' + str(new_arrivals) + '/' + str(len(completed_arrivals)) + '/' + str(len(arrivals)), end='')

    except:
      print(airport + ' failed.')

    finally:
      if 'cxn' in locals() or 'cxn' in globals(): cxn.close()