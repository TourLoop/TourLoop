#!/bin/bash

# original command to get OSM edmonton data
curl https://overpass-api.de/api/map?bbox=-113.7155,53.3971,-113.3161,53.6482 --output edmonton-OSM-data.xml

# format of overpass API:
#left,bottom,right,top
#top: 53.6482
#left: -113.7155
#right: -113.3161
#bottom: 53.3971
#
