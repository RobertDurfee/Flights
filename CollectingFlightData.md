# Collecting Flight Data

## Configuring

Before moving forward, create a [Google Cloud Platform](https://cloud.google.com) account. If you haven't created one before, you should be able to get a free $300 credit and 365 days to use it. Once your account is set up, download and install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-windows). 

Once everything is installed, initialize GCloud and create a new project. Start with the command
```
gcloud init
```
After you enter this command. Google will walk you through logging into your account and then ask you to select or create a new project. Be sure to create a new project (if you happen to have any projects already on your account). I created a new project with the following ID
```
flights-v4eqvci
```
Then, you need to enable billing in order to proceed with creating storage buckets and virtual machines. Unfortunately, there is no command (that I am aware of) to enable billing. So, just follow the [Modify a Project's Billing Settings](https://cloud.google.com/billing/docs/how-to/modify-project) tutorial to link a billing account to your project.

### Google Cloud Storage

After the project has been created, we need to create a storage bucket. First, enable the Storage API
```
gcloud services enable storage-component.googleapis.com
gcloud services enable storage-api.googleapis.com
```
After this completes, enter
```
gsutil mb -p flights-v4eqvci -c regional -l us-central1 gs://flights-radar/
```
This will create a `flights-radar` regional storage bucket in Iowa. You can learn about other [classes](https://cloud.google.com/storage/docs/storage-classes) and [locations](https://cloud.google.com/storage/docs/locations#location-r) and choose one that fits your needs (or budget) best.

### Google Cloud Compute Engine

First, enable the Compute Engine API
```
gcloud services enable compute.googleapis.com
```
Then, we can create a small Debian virtual machine with the command
```
gcloud compute instances create flights-instance --image-project=debian-cloud --image-family=debian-9 --boot-disk-size=10GB --boot-disk-type=pd-standard --machine-type=f1-micro --zone=us-central1-a
```
You can view different images to choose from by running
```
gcloud compute images list
```
Different machine types with
```
gcloud compute machine-types list
```
And different zones with the command
```
gcloud compute zones list
```
Be sure to be aware of how much different settings will cost, though! These were specifically chosen to minimize cost and are more than capable to handle our use case.

To connect to the instance, run
```
gcloud compute ssh flights-instance
```

### GitHub

To make development easier, we are going to use a git repository to sync changes between our local machine and the server instance. First, create a [GitHub Account](https://github.com/join). After your account is created, [create](https://github.com/new) a new public `Flights` repository.

Ensure `git` is installed on your machine by following [this guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Then, run the following command on both your local computer and the virtual machine created above to clone the new repository
```
git clone https://github.com/RobertDurfee/Flights.git
```
After replacing `RobertDurfee` with your username, of course, unless you want all the work done for you.

## Radar Maps

The first piece of data we want to start collecting are real-time snapshots of weather radar. The link we are going to query is `http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmsir{STATE}_.gif` where `{STATE}` can be one of the following:

- `il` for Illinois
- `wi` for Wisconsin
- `mn` for Minnesota
- `ia` for Iowa
- `mo` for Missouri
- `ky` for Kentucky
- `in` for Indiana
- `mi` for Michigan

There are many more possible state codes, but we will primarily focus on the Illinois area as we will be predicting Chicago O'Hare flight delays and cancellations.

Every $15$ minutes, these maps will be replaced with the most current. Therefore, we will query each map URL every $15$ minutes and download the map. Once we download the map, we will transfer the image to our `flights-radar` storage bucket.

### Downloading Images

To download the maps, we will use the `requests` Python library. To install this library, run the command
```
pip install --upgrade requests
```
Once the library is installed, take a look at the following function.
```py
import requests
from datetime import datetime

def fetch(state):

  response = requests.get(f'http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmsir{state}_.gif', stream=True)

  map_gif = b''  # the 'b' prefix lets Python know the string is binary.

  for chunk in response:
    map_gif += chunk

  return map_gif
```

### Uploading Images

To upload the map, we will use the `google.cloud.storage` Python library. To install this library, run the command
```
pip install google-cloud-storage
```
In order for the client to function, authentication needs to be set up. Run the following commands to set up a service account.
```
gcloud iam service-accounts create flights-service-account
gcloud projects add-iam-policy-binding flights-v4eqvci --member "serviceAccount:flights-service-account@flights-v4eqvci.iam.gserviceaccount.com" --role "roles/owner"
gcloud iam service-accounts keys create flights-service-account-key.json --iam-account flights-service-account@flights-v4eqvci.iam-gserviceaccount.com
```
Make sure to add the key file to your `.gitignore` to make sure it isn't made public. Now, in order for the Python library to find the configuration, set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable by running the following for Windows (perhaps on your local machine)
```
set GOOGLE_APPLICATION_CREDENTIALS=C:\Path\To\flights-service-account-key.json
```
Or for Linux (like on the virtual machine instance),
```
export GOOGLE_APPLICATION_CREDENTIALS="/Path/To/flights-service-account-key.json"
```
Note that this only applies for the current session. If you open a new session, you need to reset this variable.

With this set up, take a look at the following function for uploading to storage buckets.
```py
from google.cloud import storage

def upload(data, content_type, bucket, filename):

  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket)
  blob = bucket.blob(filename)
  blob.upload_from_string(data, content_type)
```

### Putting it Together

With these two functions, we can write a script to get the latest radar maps for all the desired states. 
```py
if __name__ == '__main__':

  states = { 'il': 'Illinois', 'wi': 'Wisconsin', 'mn': 'Minnesota', 'ia': 'Iowa', 'mo': 'Missouri', 'ky': 'Kentucky', 'in': 'Indiana', 'mi': 'Michigan' }

  for state in states:

    radar_gif = fetch(state)

    filename = states[state] + '/' + state.upper() + datetime.now().strftime('%Y%m%dT%H%M%S') + '.gif'

    upload(radar_gif, 'image/gif', 'flights-radar', filename)
```
But remember that this will fail without the correct credentials. Be sure to run `gcloud init` on all machines as well as all the subsequence commands specified above. Once this is done, we need to set the environment variable before every run of the Python script. To do this, we will use a very simple bash script
```sh
#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="/home/rober/Flights/flights-service-account-key.json"

date=$(date +%Y%m%dT%H%M%S)
printf $date

/usr/bin/python3.5 /home/rober/Flights/Radar/collect_radar.py || { printf " Failed\n" ; exit 1; }

printf " Success\n"
```
Be sure to make this script executable by calling
```sh
chmod u+x collect_radar.sh
```

To ensure access to the bucket, run
```
gsutil acl ch -u flights-service-account@flights-v4eqvci.iam.gserviceaccount.com:WRITE gs://flights-radar
```

Now, we want to call this script every fifteen minutes. To do this, we will create a cron job. To edit the crontab, run
```
sudo crontab -e
```
And then enter the following line at the end of the file
```
*/15 * * * * /bin/bash /home/rober/Flights/Radar/collect_radar.sh >>/home/rober/Flights/Radar/status.log 2>&1
```
### SQL Instance

Using the following command, create a shared-cpu SQL instance on Google Cloud Platform
```
gcloud sql instances create flights-database --authorized-networks=35.192.155.237 --no-backup --database-version=MYSQL_5_7 --gce-zone=us-central1-a --region=us-central1 --storage-size=10 --storage-type=HDD --tier=db-f1-micro
```

Install the `mysql` client to set up the radar database
```
sudo apt install mysql-client
```
Once this is installed, we can write the following script
```sql
CREATE DATABASE `FlightsDatabase`;
USE `FlightsDatabase`;

CREATE TABLE `Radar` (
  `RadarID` int NOT NULL AUTO_INCREMENT,
  `CreatedDateTime` DATETIME(6),
  `State` VARCHAR(50),
  `URL` VARCHAR(100),
  PRIMARY KEY (`RadarID`)
);

CREATE UNIQUE INDEX `UQ_Radar_CreatedDateTime_State` ON `Radar`(`CreatedDateTime`, `State`);
```
Execute this script by launching the `mysql` client,
```
mysql --host=146.148.73.209 -u root
```
And then typing
```
source CreateFlightsDatabase.sql
source CreateRadarTable.sql
```

Once this is in place, we can set up the Python client
```
pip install --upgrade mysql-connector-python
```
Now, we can create the following function to insert the data into the SQL databse
```py
def insert(cxn, data):

  cursor = cxn.cursor()

  query = '''
    INSERT INTO `Radar` (`CreatedDateTime`, `State`, `URL`)
    VALUES (%(CreatedDateTime)s, %(State)s, %(URL)s)
    '''

  cursor.execute(query, data)

  cxn.commit()
  cursor.close()
```
Then, our main script becomes
```py
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
```
Now the radar map collection process is complete!