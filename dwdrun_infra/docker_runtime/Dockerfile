#Dockerfile
FROM python:3.11
# Install additional dependencies
ENV DOCKER_CONTAINER=true

# Install dependencies
COPY ./dwdrun_infra/docker_runtime/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Set up the application
COPY /python_codebase/ /python_codebase/
COPY ./dwdrun_infra/__init__.py /

# forward request and error logs to docker log collector
RUN ln -sf /proc/1/fd/1 /var/log/test.log

# Set the working directory
WORKDIR /python_codebase

ENTRYPOINT [ "python", "-u", "./dwdrun/runner.py" ]
