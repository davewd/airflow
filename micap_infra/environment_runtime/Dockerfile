#Dockerfile
FROM python:3.13.2

# Install additional dependencies and Poetry
ENV DOCKER_CONTAINER=true
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 -

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set up working directory
WORKDIR /app

# Copy project files for dependency installation
COPY pyproject.toml poetry.lock ./

RUN echo|pwd
RUN echo|ls -R

# Install dependencies (without AI group since it's not compatible with Python 3.13)
RUN poetry install --without ai --no-interaction

# Copy application code
COPY ../../source/ source/
COPY ../../airflow_dags/ airflow_dags/
COPY ../../micap_infra/ micap_infra/

RUN echo|pwd
RUN echo|ls -R

# forward request and error logs to docker log collector
RUN ln -sf /proc/1/fd/1 /var/log/test.log

ENTRYPOINT [ "poetry", "run", "python", "-u", "source/micap_runtime/runner.py" ]
