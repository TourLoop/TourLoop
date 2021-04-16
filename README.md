# TourLoop

The #1 loop generating map in the world.

# Notes for the ECE 493 Marking Team

### Deploying the application

TourLoop is a complicated application, and there is a significant amount of setup required to run the application. It is very difficult for us to write setup instructions that will work on everyones computer. We cannot anticipate the bugs that may arise from different version of operating systems, docker, python or other technologies used.

To make it easy to test the functional requirements we have deployed TourLoop to http://162.246.157.222:5000 and plan to keep the web application running for serveral weeks after the course. If you would like to run TourLoop locally we have included steps to run the application below. Please feel free to contact us via email if you run into any issues.

### Notes on Testing the Functional Requirements

The underlying OpenStreetMap data is disconnected. This can lead to the search algorithms occasionally not finding a route as they are stuck in a disconnected island. Handling disconnected sections of the OpenStreetMap data was not included in the SRS and we are only required to display a no route found error (FR5).

FR3 Closest Node Point can only be tested indirectly through user interface. Everytime a route is generated we start the search algorithm at the closest node to the user specified start location.

FR5 No Route Error can be confirmed using start location 53.566845, -113.541152, target route distance 2, path type bike and algorithm 2.

For FR9 Route Generation Randomness only algorithm 3 is random. This functional requirement can usually be confirmed by generating multiple routes with algorithm 3 and the same route preferences. The route preferences start location 53.510339, -113.536677, target route distance 3.5, path type paved road and algorithm algorithm 3 work well for demonstrating the randomness.

FR10 Path Preference can be confirmed using the route preferences start location 53.521724, -113.486071, target route distance 2, and algorithm type algorithm 2. Switching between path type bike and path type paved road demonstrates the functionality.

Instructions for FR17 Clean OpenStreetMap Data and FR18 Rebuild Database are described Build-n-run the DB section of this README.

# Local Build Instructions

### Create a config.py file

Create a file called config.py in the folder server/instance/config.py
Note you may need to create the instance folder as well.

In the config.py file add the following lines:

DATABASE_SECRET_KEY = "test"
DATABASE_USERNAME = "neo4j"
DATABASE_URL = "bolt://localhost:7687"

Save the config.py file.

### system requirements

- docker
- docker-compose
- python3
- bash
- npm & nodejs

For optimal performance, docker containers should have access to 4GB of RAM. Change this on your docker settings.
You may also need to run the deploy script with 'sudo' in order to run docker commands.

### Run the Deploy Script

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

### Success?

If successfull TourLoop should be running at http://localhost:5000/.

# Build-n-run the DB

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
Once the database is created run the following to create indices and delete single nodes.

```
python3 index_creator.py
```

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
