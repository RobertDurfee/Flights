#!/bin/sh

date=$(date +%Y%m%dT%H%M%S)
printf $date

/usr/bin/python3.5 /home/rober/Flights/METAR/collect_METAR.py || { printf " Failed\n" ; exit 1; }

printf " Success\n"
