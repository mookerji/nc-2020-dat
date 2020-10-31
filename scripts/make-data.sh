#! /bin/env bash

ZIP_FILE=data/ZIP_Code_Tabulation_Areas-shp/ZIP_Code_Tabulation_Areas.shp
ABM_FILE=limbo/absentee_20201103-stripped.csv

mkdir -p limbo/

python3 ncdat/plot_abm_cancels.py --zip-file "$ZIP_FILE" --filename "$ABM_FILE" --party Democrats
python3 ncdat/plot_abm_cancels.py --zip-file "$ZIP_FILE" --filename "$ABM_FILE" --party Unaffiliated

python3 ncdat/one_stop_locations.py

python3 ncdat/plot_county_one_stop.py --filename "$ABM_FILE"
python3 ncdat/plot_abm_latency.py --filename "$ABM_FILE"
python3 ncdat/plot_accepted.py  --filename "$ABM_FILE"
