import requests
from datetime import datetime
from google.cloud import storage
import mysql.connector


def fetch(state):

  response = requests.get('http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmsir' + state + '_.gif', stream=True)

  map_gif = b''  # the 'b' prefix lets Python know the string is binary.

  for chunk in response:
    map_gif += chunk

  return map_gif


def upload(data, content_type, bucket, filename):

  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket)
  blob = bucket.blob(filename)
  blob.upload_from_string(data, content_type)


def insert(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Radar` (`CreatedDateTime`, `State`, `URL`)
    VALUES (%(CreatedDateTime)s, %(State)s, %(URL)s)
    '''

  cursor.execute(query, data)

  cxn.commit()
  cursor.close()


if __name__ == '__main__':

  states = {
    'al': 'Alabama',      'ar': 'Arkansas',      'az': 'Arizona',     'co': 'Colorado', 
    'ct': 'Connecticut',  'fl': 'Florida',       'ga': 'Georgia',     'ia': 'Iowa', 
    'id': 'Idaho',        'il': 'Illinois',      'in': 'Indiana',     'ks': 'Kansas', 
    'ky': 'Kentucky',     'la': 'Louisiana',     'mi': 'Michigan',    'mn': 'Minnesota',
    'mo': 'Missouri',     'ms': 'Mississippi',   'mt': 'Montana',     'nd': 'NorthDakota',
    'ne': 'Nebraska',     'nh': 'NewHampshire',  'nm': 'NewMexico',   'nv': 'Nevada', 
    'ny': 'NewYork',      'oh': 'Ohio',          'ok': 'Oklahoma',    'or': 'Oregon', 
    'pa': 'Pennsylvania', 'sc': 'SouthCarolina', 'sd': 'SouthDakota', 'tn': 'Tennessee', 
    'ut': 'Utah',         'va': 'Virginia',      'wa': 'Washington',  'wi': 'Wisconsin',
    'wy': 'Wyoming'
  }

  for state in states:

    try:

      cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='Radar')

      radar_gif = fetch(state)

      now = datetime.now()
      filename = states[state] + '/' + state.upper() + now.strftime('%Y%m%dT%H%M%S') + '.gif'
      url = 'gs://flights-radar/' + filename

      upload(radar_gif, 'image/gif', 'flights-radar', filename)
      insert(cxn, { 'CreatedDateTime': now, 'State': states[state], 'URL': url })

    except:
      print(state + ' failed.')
  
    finally:
      if 'cxn' in locals() or 'cxn' in globals(): cxn.close()
