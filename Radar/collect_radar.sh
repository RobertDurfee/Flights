#!/bin/sh

export GOOGLE_APPLICATION_CREDENTIALS="/home/rober/Flights/flights-service-account-key.json"

python3 /home/rober/Flights/Radar/collect_radar.py
