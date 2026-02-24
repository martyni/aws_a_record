#!/bin/bash -x
source scripts/common.sh
docker run ${DOCKER_FLAGS} ${DOCKER_REPO}/${NAME}:${VERSION}|| (echo -e "fail to start container\n" >>${OUTPUT})
curl --fail -i -H "Content-Type: application/json" --data '{"user":"alex","message":"Hi everyone! Alex here"}' localhost:5000/message || echo -e "fail to send message\n" >>${OUTPUT}
docker stop $(docker ps | awk  "/${DOCKER_REPO}\/${NAME}/{print \$1}")&

#Delete all non up containers
#docker rm $(docker ps -a | grep -v Up |grep -v CONTAINER| awk '{print $1}' )
