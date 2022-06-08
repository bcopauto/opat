#!/bin/bash

echo "Date Extraction started!"
awk -F "\"*,\"*" '{print $2}' logana/processes/semiPreparedTemp.csv > logana/processes/dates.csv
echo "Date Extraction Ended!"
