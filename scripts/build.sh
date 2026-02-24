#!/bin/bash
source scripts/common.sh

docker_build () {
   pwd
   cp /tmp/*.pem .
   unbuffer ${BUILD_COMMAND}
   echo -e ${RUN_COMMAND}
   rm *.pem
}


local_build () {
   pip install .
}


docker_build && local_build
