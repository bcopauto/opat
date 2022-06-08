#!/bin/bash

echo "Date Extraction started!"
awk -F "\"*,\"*" '{print $2}' logana/processes/results/final.csv > logana/processes/results/dates.csv
echo "Date Extraction Ended!"
echo "Removing splitted dates"
rm -rf logana/processes/splittedDates.csv

