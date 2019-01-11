#!/bin/sh

date=$(date +%Y%m%dT%H%M%S)
printf $date

/usr/bin/python3.5 /home/rober/Flights/TAF/collect_TAF.py || { printf " Failed\n" ; exit 1; }

printf " Success\n"
