#!/bin/bash

for f in results/*.csv
do 
	echo "Processing $f file.."
	mongoimport -d nfl -c receiving --type csv --file $f --headerline
done
