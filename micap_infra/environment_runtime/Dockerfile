#Dockerfile
FROM python:3.13
# Install additional dependencies
ENV DOCKER_CONTAINER=true

# Install dependencies
COPY ./micap_infra/environment_runtime/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Set up the application
COPY /source/ /source/
COPY ./source/__init__.py /

# forward request and error logs to docker log collector
RUN ln -sf /proc/1/fd/1 /var/log/test.log

# Set the working directory
WORKDIR /source

ENTRYPOINT [ "python", "-u", "./micap_runtime/runner.py" ]
