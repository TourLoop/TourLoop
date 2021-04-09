#!/bin/bash

# get production version of front end (if not uploaded already)
cd client
npm install && npm run build
cd ../

# skip this step by pre-downloading edmonton-OSM-data.xml into raw-data from:
# <google-drive-link>
# get the original datafile
# if not already there
if [ ! -f ./raw-data/edmonton-OSM-data.xml ]; then
    cd raw-data
    echo "Database file not found... downloading from overpass API"
    ./download.sh
    cd ../
fi

# rebuild the database (prepare for it at least)
cd database
./rebuild-database-files.sh
cd ../

# docker up the services
docker-compose up -d --build

# auto-add the neo4j indexes
sleep 30s
cd database
python3 index_creator.py
# if that failed, wait a bit then retry
