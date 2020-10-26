#! /bin/env bash

# Download one-stop locations
curl https://vt.ncsbe.gov/OSSite/GetStatewideList/ > ./data/one-stop-absentee/StatewideList.txt

# Download party change list
curl -vk https://dl.ncsbe.gov.s3.amazonaws.com/data/PartyChange/2020_party_change_list.csv \
     > data/changes/2020_party_change_list.csv

# Download
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ENRS/2020_11_03/absentee_demo_stats_20201103.csv > limbo/absentee_demo_stats_20201103.csv

# Get absentee votes
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ENRS/2020_11_03/absentee_20201103.zip > limbo/absentee_20201103.zip

unzip -o limbo/absentee_20201103.zip -d limbo/

bash scripts/clean-unicode.sh limbo/absentee_20201103.csv > limbo/absentee_20201103-stripped.csv

# Get precincts (Mecklenburg County)
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ShapeFiles/Precinct/MECKLENBURG_PRECINCTS_KML.kml > limbo/MECKLENBURG_PRECINCTS_KML.kml

# Precincts
curl -vk https://dl.ncsbe.gov.s3.amazonaws.com/ShapeFiles/Precinct/SBE_PRECINCTS_20201018.zip > limbo/SBE_PRECINCTS_20201018.zip

curl -v https://s3.amazonaws.com/dl.ncsbe.gov/ENRS/2020_11_03/polling_place_20201103.csv \
     >  data/election-day-precincts/polling_place_20201103.csv
