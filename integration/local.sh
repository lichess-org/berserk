#!/bin/bash -e

integration_test() {
    # BDIT = Berserk Docker Image Test, trying to reduce collision
    local BDIT_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local BDIT_IMAGE=ghcr.io/lichess-org/lila-docker:main
    local BDIT_LILA=bdit_lila
    local BDIT_NETWORK=bdit_lila-network
    local BDIT_APP_IMAGE=ghcr.io/astral-sh/uv:debian
    local BDIT_APP=bdit_app

    cleanup_containers() {
        docker rm --force $BDIT_LILA > /dev/null 2>&1 || true
        docker rm --force $BDIT_APP > /dev/null 2>&1 || true
        docker network rm $BDIT_NETWORK > /dev/null 2>&1 || true
    }

    echo "Running integration tests"
    cleanup_containers

    docker network create $BDIT_NETWORK
    docker build -f "$BDIT_SCRIPT_DIR/Dockerfile" "$BDIT_SCRIPT_DIR/.." --build-arg UV_CACHE_DIR="$HOME/.cache/uv" -t bzrk
    docker run --name $BDIT_LILA --network $BDIT_NETWORK -d $BDIT_IMAGE
    docker run --name $BDIT_APP --network $BDIT_NETWORK bzrk

    cleanup_containers
    echo "✅ Done"
}
integration_test