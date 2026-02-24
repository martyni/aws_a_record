#!/bin/bash
if [[ -z $(which unbuffer) ]]; then
    echo Running in a pipeline Colour not set
    export PIPELINE=1
else
    echo Running locally setting Colour Variables
    export GREEN='\033[0;32m'
    export RED='\033[0;31m'
    export YELLOW='\033[0;33m'
    export NO_COLOUR='\033[0m'
fi

export RUN_DIR=$(realpath $(dirname $0))
export BUILD_EXIT_FILE=/tmp/build_exit_code
export BUILD_OUTPUT=/tmp/build_output
export DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
export DOCKER_REPO=$(cat ${RUN_DIR}/DOCKER_REPO)
export NAME=$(cat ${RUN_DIR}/NAME)
export FULL_NAME="${DOCKER_REPO}/$(cat ${RUN_DIR}/NAME)"
export VERSION=$(cat ${RUN_DIR}/VERSION)
export DESCRIPTION=$(cat ${RUN_DIR}/DESCRIPTION)
export DOMAIN=$(cat ${RUN_DIR}/DOMAIN)
export BUILD_COMMAND="docker build  . -t ${DOCKER_REPO}/${NAME}:${VERSION}"
export RUN_COMMAND="docker run ${DOCKER_FLAGS} ${DOCKER_REPO}/${NAME}:${VERSION}"
export CURRENT_TEST=None
export OUT=/tmp/output
export OLD_VERSION=$(cat ${RUN_DIR}/VERSION)
export INCREMENT=$(git rev-parse --abbrev-ref HEAD | awk -F "/" '{ print $1}')
export SEMVER="/usr/bin/semver"
export COMMIT_MESSAGE=$(git log -1 --pretty=%B)
export PORT=$(cat ${RUN_DIR}/PORT)
