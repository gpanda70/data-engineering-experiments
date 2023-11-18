#!/bin/bash

# Specify the neo4j image you want to check and possibly pull
IMAGE_NAME="neo4j:5.13.0-enterprise"

# Check if the Docker image exists locally
if ! docker image inspect "$IMAGE_NAME" > /dev/null 2>&1; then
    echo "Image $IMAGE_NAME does not exist locally. Pulling..."
    docker pull "$IMAGE_NAME"
    echo "Pull complete."
else
    echo "Image $IMAGE_NAME already exists locally. No pull required."
fi

# Start container
docker run -it --rm \
    --publish=7474:7474 --publish=7687:7687 --publish=7473:7473\
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    --env NEO4J_PLUGINS='["graph-data-science", "apoc", "apoc-extended"]' \
    $IMAGE_NAME