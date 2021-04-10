#!/bin/bash

# TOURLOOP FR18 : Rebuild database

# fail if one command fails
set -e

echo "parsing xml file (~1 min?)"
time python3 osm_xml_to_csv.py

echo "move csv files to loading area"
mv osm-ways.csv docker-stuff/database-files/
mv osm-nodes.csv docker-stuff/database-files/

echo "compress csv files for server export"
mkdir -p ../server/instance || true
cd docker-stuff
tar -cvzf tourloop-database.tar.gz database-files/*
mv tourloop-database.tar.gz ../../server/instance

echo "save all path and all bike path results"
mv ../all_dirt_paths.txt ../../server/instance
mv ../all_bike_paths.txt ../../server/instance
mv ../all_paved_paths.txt ../../server/instance
cd ../
