#!/bin/bash



awk '{ print $1 } ' logana/processes/bots.log
awk '{ print $1 } ' logana/processes/bots.log | sort
awk '{ print $1 } ' logana/processes/bots.log | sort | uniq > logana/processes/uniq.txt

