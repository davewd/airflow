#Dockerfile
FROM python:3.11
# Install additional dependencies
#USER root
COPY /infra/docker_runtime/requirements.txt ./requirements.txt

#USER airflow
RUN pip install --user --upgrade pip
# Set up additional Python dependencies
RUN pip install -r ./requirements.txt

CMD echo ${PWD}
CMD ls -ltr

## Copy in changed code layer.
COPY python_codebase ./python_codebase/

CMD ls -ltr
ENTRYPOINT [ "python", "./python_codebase/dwdrun/run.py" ]
