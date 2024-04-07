__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from datetime import datetime

@dag(start_date=datetime(2023, 1 , 1), schedule='@daily', catchup=True)
def parallel_dag():

    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 60'.format(t)) for t in range(1, 4)]

    @task
    def task_4(data):
        print(data)
        return 'done'
    
    @task
    def task_5(data):
        print(data)

    tasks >> task_5(task_4(42))

parallel_dag()