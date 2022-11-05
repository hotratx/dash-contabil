# pull official base image
FROM python:3.10.8-bullseye

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql curl python3-dev fonts-liberation fonts-recommended openjdk-17-jre openjdk-17-jdk locales locales-all\
  && apt-get clean
ENV PATH "${PATH}:/usr/bin/java"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Looks like poetry fails to add itself to the Path in Docker. We add it here.
ARG INSTALL_DEV=true
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH "${PYTHONPATH}:/app"
# ENV PATH $PATH:/usr/bin/java
EXPOSE 8080


ENV LC_ALL pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8

COPY . .
