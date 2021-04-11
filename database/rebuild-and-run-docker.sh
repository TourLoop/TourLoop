#!/bin/bash

# TOURLOOP FR18 : Rebuild database

# fail if one command fails
set -e

echo "parsing xml file (~3 min?)"
time python3 osm_xml_to_csv.py

echo "starting container construction"
mv osm-ways.csv docker-stuff/database-files/
mv osm-nodes.csv docker-stuff/database-files/

# TODO: refactor script to account for new docker-compose location
echo "Stop any existing db containers and reubild one (~3 min?)"
cd docker-stuff
docker-compose down
docker-compose up --build -d

echo "compress csv files for server export"
mkdir -p ../server/instance || true
tar -cvzf tourloop-database.tar.gz database-files/*
mv tourloop-database.tar.gz ../../server/instance

echo "save all path and all bike path results"
mv ../all_dirt_paths.txt ../../server/instance
mv ../all_bike_paths.txt ../../server/instance
mv ../all_paved_paths.txt ../../server/instance

echo "container should be running..."
echo "localhost:7474 will be available within the next 30s"

