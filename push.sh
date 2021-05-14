#!/bin/bash
#
# Build production image from the currently checked out version
# of ListenBrainz and push it to Docker Hub, with an optional
# tag (which defaults to "beta")
#
# Usage:
#   $ ./push.sh [tag]

set -e

cd "$(dirname "${BASH_SOURCE[0]}")/"

TAG=${1:-beta}
echo "building for tag $TAG"
docker build -t kartik1712/metric-writer:"$TAG" . && \
    docker push kartik1712/metric-writer:"$TAG"
