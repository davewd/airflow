#!/bin/bash
echo building Docker Images
cd ./docker_runtime/
bash ./build_infra.sh
cd ..
echo Starting AIRFLOW UI webserver

#docker network create dwdrunnetwork
cd ./airflow_infra_config/
docker-compose up

echo started With process ID
