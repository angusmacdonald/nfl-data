#!/bin/bash

mongoimport -d nfl -c teams --type csv --file team-data.csv --headerline
