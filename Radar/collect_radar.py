import requests
from datetime import datetime
from google.cloud import storage


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


if __name__ == '__main__':

  states = { 'il': 'Illinois', 'wi': 'Wisconsin', 'mn': 'Minnesota', 'ia': 'Iowa', 'mo': 'Missouri', 'ky': 'Kentucky', 'in': 'Indiana', 'mi': 'Michigan' }

  for state in states:

    radar_gif = fetch(state)

    filename = states[state] + '/' + state.upper() + datetime.now().strftime('%Y%m%dT%H%M%S') + '.gif'

    upload(radar_gif, 'image/gif', 'flights-radar', filename)
