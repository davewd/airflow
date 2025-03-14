#!/bin/bash

echo Stopping all dwdrun infra services

cd ./dwdrun_infra_config/
docker-compose down 
