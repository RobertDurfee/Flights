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

  cxn = mysql.connector.connect(host='146.148.73.209', user='root', db='FlightsDatabase')

  states = { 'il': 'Illinois', 'wi': 'Wisconsin', 'mn': 'Minnesota', 'ia': 'Iowa', 'mo': 'Missouri', 'ky': 'Kentucky', 'in': 'Indiana', 'mi': 'Michigan' }

  for state in states:

    radar_gif = fetch(state)

    now = datetime.now()
    filename = states[state] + '/' + state.upper() + now.strftime('%Y%m%dT%H%M%S') + '.gif'
    url = 'gs://flights-radar/' + filename

    upload(radar_gif, 'image/gif', 'flights-radar', filename)
    insert(cxn, { 'CreatedDateTime': now, 'State': states[state], 'URL': url })
  
  cxn.close()
