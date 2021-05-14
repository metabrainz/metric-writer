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

GIT_COMMIT_SHA="$(git describe --tags --dirty --always)"

TAG=${1:-beta}
echo "building for tag $TAG"
docker build \
    --tag metabrainz/metric-writer:"$TAG" \
    --build-arg GIT_COMMIT_SHA="$GIT_COMMIT_SHA" . && \
    docker push metabrainz/metric-writer:"$TAG"
