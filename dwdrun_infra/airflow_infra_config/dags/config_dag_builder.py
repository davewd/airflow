__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"


from pathlib import Path
import pendulum
import yaml
import airflow
from airflow.decorators import dag
from airflow import DAG
from airflow.utils.task_group import TaskGroup
import os
from constants import ConfigurationFileTypeEnum
from airflow.operators.empty import EmptyOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash import BashOperator
import datetime

""" def create_parallel_groups():
        for source in sources:
            source = source.replace("\\", ".")
            with TaskGroup(group_id=source) as task_group:
            extract = ExtractOperator(task_id="extract", source=source)
            transform = TransformOperator(task_id="transform", source=source)
            load = LoadOperator(task_id="load", source=source)
            extract >> transform >> load
        return task_group
 """


def clean_task_name(input_path):
    removed_suffix_clean = input_path.replace(".yml", "")
    removed_suffix_clean = removed_suffix_clean.replace(".yaml", "")
    cleaned_path = removed_suffix_clean.replace("/", ".")
    return cleaned_path


def read_files_in_folders_recursively(folder_path):
    for root, dirs, files in os.walk(folder_path):

        # Each Folder is a DAG.
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            dag = len(relative_path.split(os.sep))
            dag_parent_name = relative_path.split(os.sep)[0]
            # assumes sequential os walk.
            if dag == 2:
                dag_parent = DAG(
                    dag_id=dag_parent_name,
                    start_date=datetime.datetime(2024, 1, 1),
                    schedule="@daily",
                )

            with open(file_path, "r") as config_file:
                sources_config = yaml.safe_load(config_file) or {}
                # file_type = #TODO: Allow ability for DEFAULTS File to store defaults at a level.

                jobCommandType = sources_config.get("jobCommandType")
                file_type = ConfigurationFileTypeEnum.UNKNOWN
                if jobCommandType == "dwdrun":
                    file_type = ConfigurationFileTypeEnum.TASK

                if file_type == ConfigurationFileTypeEnum.UNKNOWN:
                    EmptyOperator(task_id=clean_task_name(relative_path), dag=dag_parent)
                elif file_type == ConfigurationFileTypeEnum.TASK:
                    jobCommand = sources_config.get("jobCommand")
                    jobCommandNamedParams = sources_config.get("jobCommandNamedParams")
                    DockerOperator(
                        task_id=clean_task_name(relative_path),
                        image="dwdrun",
                        api_version="auto",
                        auto_remove=True,
                        command=f"--jobModule={jobCommand} --runDate={{ds}}",  # TODO {jobCommandNamedParams}",
                        docker_url="unix://var/run/docker.sock",
                        network_mode="dwdrunnetwork",
                        dag=dag_parent,
                    )
                    # touch
                elif file_type == ConfigurationFileTypeEnum.PARALLEL_TASK:
                    jobCommand = sources_config.get("jobCommand")
                    jobCommandNamedParams = sources_config.get("jobCommandNamedParams")
                    BashOperator(
                        task_id=clean_task_name(relative_path),
                        bash_command=f"dwdrun.sh --jobModule={jobCommand} --runDate={{ds}} {jobCommandNamedParams}",
                        dag=dag_parent,
                    )
                elif file_type == ConfigurationFileTypeEnum.PARALLEL_TASK_GENERATOR:
                    print(f"Generate me a big task please with a name {'123'}")
                else:
                    print(f"Shiiiiiit. {'234'}")

                print(f"{relative_path} - {dirs} - {file}")
                print(sources_config)

            globals()[dag_parent_name] = dag_parent


current_folder_path = os.path.dirname(os.path.abspath(__file__))
folder_path = f"{current_folder_path}/config/"
read_files_in_folders_recursively(folder_path)
# Cross Dags can use : ExternalTaskSensor
