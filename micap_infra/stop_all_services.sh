#!/bin/bash

echo Stopping all dwdrun infra services

cd ./environment_services/
docker-compose down 
