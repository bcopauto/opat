#!/bin/bash
{ head -q -n 2 ./results/augDates.csv && tail -n 1 ./results/augDates.csv } > ./results/flast.csv
