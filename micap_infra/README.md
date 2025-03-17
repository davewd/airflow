# Infra

## TL/DR
- Run start_all_services.sh and it will auto configure the environmnet to run.


## Full infra
- airflow Scheduler
- airflow UI
- airflow worker
- gitSynch (https://github.com/data-burst/airflow-git-sync)
- flower (airflow worker monitor)
- dag updator from gihthub
- mongo cluster


### docker_runtime
Simple Dockerfile to take input params and start the entry point into the pyhton code base.
Should pass through jobModule + runDate + all named Args 

dwd_run is the shell entry point (to be called from within airflow BASH operator)

airflow (runDate + job module) -> Bash (confert to standard entry point) -> Docker (runtime environment) -> Python 'runner' (actually do the work, start in python world)

