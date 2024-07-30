# CODING - SCHEDULING

## Goal
`Outcome: send myself a quote everyday @ 7am.`

## Research to do this in cloud

How to run an airflow instance as a hobbyist:
MWAA = 4k
Azzure 0.49 per hour. = 4k
pythonanywhere - low cpu time.

So go local, put up with downtime..... always on local host.
https://marclamberti.com/blog/airflow-on-kubernetes-get-started-in-10-mins/

## Background Learning / Refresh
- Brew
- Docker: https://www.youtube.com/watch?v=pg19Z8LL06w
- Docker-compose: https://www.youtube.com/watch?v=SXwC9fSwct8
- airflow:
- mongo:


## Setup Machine with required Items

### Base machine requirements
- brew install python
- brew install git
- brew install --cask visual-studio-code

#### Pre-requisites:
- docker -> website dmg
- brew install go
- go install sigs.k8s.io/kind@v0.18.0
- Brew install kind
- brew install helm
- brew install kubectl

code to run:
kind create cluster --name airflow-cluster --config kind-cluster.yaml

kubectl create namespace dwd-airflow

## Checks
kubectl get namespaces  #Check creation
kubectl get nodes -o wide



## HELM
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow
helm install airflow apache-airflow/airflow --namespace dwd-airflow --debug
kubectl get pods -n dwd-airflow

helm ls -n dwd-airflow


## AIRFLOW UI:
To Restart UI Run this command:
> kubectl port-forward svc/airflow-webserver 8080:8080 -n dwd-airflow --context kind-airflow-cluster
> http://localhost:8080/

to Setup:
- Touch variables.yam
- kubectl apply -f variables.yaml
- helm upgrade --install airflow apache-airflow/airflow -n dwd-airflow -f values.yaml --debug
- kubectl apply -f pv.yaml
- kubectl apply -f pvc.yml 


Kubernetes dashboard :
### To Restart Dashboard
> kubectl proxy
> http://localhost:8001/
> http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/error?namespace=dwd-airflow


### To Setup: 
- kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
- kubectl apply -f dashboard_user.yml
- kubectl apply -f dashboard_cluster_role_binding.yml
- kubectl -n kubernetes-dashboard create token admin-user




https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md



## Enable airflow to run from git
To enable airlfow jobs to be automatially updated from github repo one must connect the two via github shared Key.

1. ssh-keygen -t ed25519 -C "davewd@me.com"
2. kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshKey=/Users/daviddawson/.ssh/id_ed25519 -n dwd-airflow
3. kubectl get secrets -n dwd-airflow

kubectl delete secret airflow-ssh-git-secret -n dwd-airflow


## To create the Docker image that will run within each airflow task
1. build_infra.sh
2. test_  .... 



## ToDo
1. Send Airflow Calendar view by email each evening
