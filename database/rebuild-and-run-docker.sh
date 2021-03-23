#!/bin/bash

# TOURLOOP FR18 : Rebuild database

# fail if one command fails
set -e

echo "parsing xml file (~1 min?)"
time python3 osm_xml_to_csv.py

echo "starting container construction"
mv osm-ways.csv docker-stuff/csv-files/
mv osm-nodes.csv docker-stuff/csv-files/

echo "Stop any existing db containers and reubild one (~3 min?)"
cd docker-stuff
docker-compose down
docker-compose up --build -d

echo "compress csv files for server export"
mkdir -p ../server/instance || true
tar -cvzf tourloop-database.tar.gz csv-files/*.csv
mv tourloop-database.tar.gz ../../server/instance

echo "container should be running..."
echo "localhost:7474 will be available within the next 30s"

