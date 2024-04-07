#Dockerfile
FROM python:3.11
# Install additional dependencies
#USER root
COPY ./dwdrun_infra/docker_runtime/requirements.txt ./requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

#USER airflow
RUN pip install --user --upgrade pip
# Set up additional Python dependencies
RUN pip install -r ./requirements.txt

CMD echo ${PWD}
CMD ls -ltr

## Copy in changed code layer.
COPY /python_codebase/ /python_codebase/
COPY ./dwdrun_infra/__init__.py .

CMD ls -ltr
ENTRYPOINT [ "python", "-u", "./python_codebase/dwdrun/runner.py" ]
