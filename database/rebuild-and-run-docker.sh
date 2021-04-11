#!/bin/bash

# TOURLOOP FR18 : Rebuild database

# fail if one command fails
set -e

./rebuild-database-files.sh

echo "Stop any existing db containers and reubild one (~3 min?)"
cd ../ # cd to top level
docker-compose down
docker-compose up --build -d

