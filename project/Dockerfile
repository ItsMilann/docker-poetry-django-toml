FROM python:3.11.7-slim as development_build

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.8.4 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./dependencies/apt-requirements.txt /usr/src/app/apt-requirements.txt

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  $(cat ./apt-requirements.txt) \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version


# set work directory
COPY pyproject.toml poetry.lock /usr/src/app/

# Install dependencies:
RUN poetry install --no-root
# copy project
COPY . /usr/src/app/