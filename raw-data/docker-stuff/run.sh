#!/bin/bash

docker stop neo || true
docker rm neo || true

docker run \
    --rm \
    --name neo \
    -p7474:7474 -p7687:7687 \
    -d \
    --env NEO4J_AUTH=neo4j/test \
    myneo4j:latest
