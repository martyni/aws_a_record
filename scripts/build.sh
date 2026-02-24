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
/bin/cat <<EOM > ${RUN_DIR}/${NAME}.service
[Unit]
Description=${DESCRIPTION}
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=${USER}
ExecStart=authbind $(which gunicorn) --certfile=/tmp/$DOMAIN.combined.pem --keyfile=/tmp/$DOMAIN.key.pem --bind 0.0.0.0:${PORT} ${NAME}.app:app
[Install]
WantedBy=multi-user.target
EOM
sudo cp ${RUN_DIR}/${NAME}.service /etc/systemd/system/
sudo cat /etc/systemd/system/${NAME}.service 
netstat -ntlp | awk /${PORT}/'{print $7}' | awk -F '/' '{print $1}' | sudo xargs kill 
sudo systemctl daemon-reload
sudo systemctl enable ${NAME}
sudo systemctl stop ${NAME}
sudo systemctl start ${NAME}
for i in {1..30}; do 
    CURL="curl https://${NAME}.${DOMAIN}:${PORT}"
    echo ${CURL}
    ${CURL} && break  
    sleep ${i}
    echo "Sleeping ${i}"
done
}


docker_build && local_build
