#!/bin/bash

# get production version of front end (if not uploaded already)
cd client
npm install && npm run build
cd ../

# skip this step by pre-downloading edmonton-OSM-data.xml into raw-data from:
# https://drive.google.com/drive/u/0/folders/1csxY4bgFG6Vt3tK8NuExde1NCZFQ3Dan
# get the original datafile
# if not already there
if [ ! -f ./raw-data/edmonton-OSM-data.xml ]; then
    cd raw-data
    echo "Database file not found... downloading from overpass API"
    ./download.sh
    cd ../
fi

# rebuild the database (prepare for it at least)
echo "generating db files, this may take a while..."
cd database
pip3 install neo4j polyline vincenty || true
./rebuild-database-files.sh
cd ../

# docker up the services
echo "Starting db and backend containers"
docker-compose up -d --build

# auto-add the neo4j indexes
echo "Adding neo4j indexes for imporoved performance"
sleep 30s
cd database
python3 index_creator.py
# if that failed, wait a bit then retry
