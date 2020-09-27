#! /bin/env bash

# Download one-stop locations
curl https://vt.ncsbe.gov/OSSite/GetStatewideList/ \
     > ./data/one-stop-absentee/StatewideList.txt

# Download
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ENRS/2020_11_03/absentee_demo_stats_20201103.csv \
     > limbo/absentee_demo_stats_20201103.csv

# Get absentee votes
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ENRS/2020_11_03/absentee_20201103.zip \
     > limbo/absentee_20201103.zip

unzip -o limbo/absentee_20201103.zip -d limbo/

bash scripts/clean-unicode.sh limbo/absentee_20201103.csv \
     > limbo/absentee_20201103-stripped.csv

# Get precincts (Mecklenburg County)
curl -k https://dl.ncsbe.gov.s3.amazonaws.com/ShapeFiles/Precinct/MECKLENBURG_PRECINCTS_KML.kml \
     limbo/MECKLENBURG_PRECINCTS_KML.kml
