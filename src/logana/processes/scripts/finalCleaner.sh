#!/bin/bash

echo "Removing splitted dates"
rm -rf logana/processes/splittedDates.csv
echo "Splitted dates removed!"
echo "Attempt to flush input foder..."
rm -rf logana/processes/input/*
echo "Input folder empty!"
