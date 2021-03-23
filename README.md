# TourLoop
The #1 loop generating map in the world.

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
