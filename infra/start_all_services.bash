#!/bin/bash

echo Starting AIRFLOW UI webserver
kubectl port-forward svc/airflow-webserver 8080:8080 -n dwd-airflow --context kind-airflow-cluster
echo started With process ID
