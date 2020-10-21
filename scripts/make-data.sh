#! /bin/env bash

ZIP_FILE=data/ZIP_Code_Tabulation_Areas-shp/ZIP_Code_Tabulation_Areas.shp
VOTE_FILE=limbo/absentee_20201103-stripped.csv

mkdir -p limbo/

python3 ncdat/plot_abm_cancels.py --zip-file "$ZIP_FILE" --filename "$VOTE_FILE" --party Democrats
python3 ncdat/plot_abm_cancels.py --zip-file "$ZIP_FILE" --filename "$VOTE_FILE" --party Unaffiliated

python3 ncdat/one_stop_locations.py
