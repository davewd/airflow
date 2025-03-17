#!/bin/bash
echo building Docker Images
cd ./environment_runtime/
bash ./build_infra.sh
cd ..
echo Starting AIRFLOW UI webserver

if [ ! "$(docker network ls | grep micapnetwork)" ]; then
    echo "Creating micap_network network ..."
    docker network create micapnetwork
else
    echo "micapnetwork network exists."
fi

#Create Server certificate and key
# Run this in the certs folder.  last updated : 5Aug25
#openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost" -nodes

#docker network create micapnetwork
cd ./environment_services/
docker-compose up -d

echo started With process ID
