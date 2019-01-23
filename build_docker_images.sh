#!/bin/bash

find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

IMAGE_NAME=swicloud_sre_solution
IMAGE_TAG=$(cat VERSION)

for PYTHON_VERSION in 2.7 3.6;
do
    docker build --build-arg PYTHON_TAG="${PYTHON_VERSION}" -t "${IMAGE_NAME}_py${PYTHON_VERSION}:${IMAGE_TAG}" .
done

docker images

# for PYTHON_VERSION in 2.7 3.6;
# do
#     echo docker run -v "${PWD}":/data:ro --rm "${IMAGE_NAME}_py${PYTHON_VERSION}:${IMAGE_TAG}"
# done