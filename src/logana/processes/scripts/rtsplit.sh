#!/bin/bash

awk -F "\"*,\"*" '{print $5}' logana/processes/bots.csv > logana/processes/rt.csv
