#!/bin/bash

# fail if one command fails
set -e

echo "parsing xml file (~1 min?)"
time python3 osm_xml_to_csv.py

echo "starting container construction"
mv osm-ways.csv docker-stuff/csv-files/
mv osm-nodes.csv docker-stuff/csv-files/

cd docker-stuff
echo "building container (~3 min?)"
time ./build.sh

echo "container built! starting container"
./run.sh

echo "container should be running..."
echo "localhost:7474 will be available within the next 30s"

