#!/bin/bash
source scripts/common.sh
VERSION_FILE=${RUN_DIR}/VERSION
${SEMVER}  ${VERSION_FILE} patch
NEW_VERSION=$(cat ${VERSION_FILE})
echo -e "Version: ${OLD_VERSION} will undergo ${INCREMENT} increment to ${NEW_VERSION}"
echo ${NEW_VERSION} > ${RUN_DIR}/VERSION
git add ${RUN_DIR}/VERSION
git tag -a ${NEW_VERSION}  -m "${COMMIT_MESSAGE}"
