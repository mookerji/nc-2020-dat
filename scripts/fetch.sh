#! /bin/env bash

# Download one-stop locations
curl https://vt.ncsbe.gov/OSSite/GetStatewideList/ \
     > ./data/one-stop-absentee/StatewideList.txt
