#!/bin/bash
echo building Docker Images
cd ./docker_runtime/
bash ./build_infra.sh
cd ..
echo Starting AIRFLOW UI webserver

if [ ! "$(docker network ls | grep dwdrunnetwork)" ]; then
    echo "Creating dwdrunnetwork network ..."
    docker network create dwdrunnetwork
else
    echo "dwdrunnetwork network exists."
fi

#Create Server certificate and key
# Run this in the certs folder.  last updated : 5Aug25
#openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost" -nodes

#docker network create dwdrunnetwork
cd ./airflow_infra_config/
docker-compose down 
