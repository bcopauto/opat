#!/bin/bash
pwd
cat logana/processes/input.log | grep -E '.bot|Bots|Bot|spider' > logana/processes/bots.log
awk '{ print $1 } ' logana/processes/bots.log
awk '{ print $1 } ' logana/processes/bots.log | sort
awk '{ print $1 } ' logana/processes/bots.log | sort | uniq > logana/processes/uniq.txt
rm -rf logana/processes/input.log
echo "input.log removed"
