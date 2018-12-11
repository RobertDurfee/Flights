#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="/home/rober/Flights/flights-service-account-key.json"

date=$(date +%Y%m%dT%H%M%S)
printf $date

/usr/bin/python3.5 /home/rober/Flights/Radar/collect_radar.py || { printf " Failed\n" ; exit 1; }

printf " Success\n"
