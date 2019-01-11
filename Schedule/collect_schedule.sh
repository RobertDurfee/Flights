#!/bin/sh

export AVIATION_EDGE_API_KEY="/home/rober/Flights/Schedule/aviation-edge-api-key"

date=$(date +%Y%m%dT%H%M%S)
printf $date

/usr/bin/python3.5 /home/rober/Flights/Schedule/collect_schedule.py || { printf " Failed\n" ; exit 1; }

printf " Success\n"
