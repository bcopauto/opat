#!/bin/bash

mysql -uroot -p --local-infile opat -e"LOAD DATA LOCAL INFILE 'final.csv' 
INTO TABLE opat.templogs
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;"

