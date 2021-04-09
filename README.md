# TourLoop
The #1 loop generating map in the world.

## Deploy instructions
In the top level of this directory run:
```bash
./deploy.sh
```

### what the script does
- compiles the front end to the client/build directory
- ensures the raw OSM-xml data is present
- rebuilds database files
- uses docker-compose to bring up the database and flask API
- waits a bit then adds indexes to the running neo4j container

### skipping downloading the osm xml raw data file
The deploy script will make a call to the OpenStreetMap overpassAPI which handles exports.
In order to skip this step, the file must already exist in the raw-data folder.
Furthermore, the file must be named exactly "edmonton-OSM-data.xml"

### A note for the ECE493 marking team
The original datafile we wrote the system on is located at:
https://drive.google.com/drive/u/0/folders/1csxY4bgFG6Vt3tK8NuExde1NCZFQ3Dan
Use this file to test the system. The file downloaded by the deploy script may not be exactly the same (due to the updates OSM puts out) as the one we developed on.
It was out of scope to handle updates from OpenStreetMaps data, so if for some reason the system encounters an error using an up-to-date version of the xml file, please switch to the original xml file located on google drive.


## Build-n-run the DB

The TourLoop database is run out of a custom docker container.
This docker container has the TourLoop version of the OpenStreetMap data already inside of it.
There are no volumes or mounts required when running the TourLoop neo4j container.
If the container is stopped, then the database is effectively deleted.
In order to change the data in the docker container, a new container must be built.
There is a script for automatically building this docker container:

```bash
cd database
./rebuild-and-run-docker.sh
```

This script also removes any running instance of the docker container.
This script deletes the database, cleans the OSM data, then creates and starts a new database container.


### Deleting an old database
Done by stopping a running TourLoop neo4j container.
This is done through:
```
cd database/docker-stuff/
docker-compose down
```

### creating a new database
Assuming the OSM data is already cleaned into CSV format, to rebuild the database run this command:
```
cd database/docker-stuff/
docker-compose up -d --build
```

### Uploading cleaned data to a database
See the dockerfile for details. Data uploading is done through a neo4j admin import of the cleaned csv files.
