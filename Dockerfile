FROM python:3.7-slim
ENV LANG C.UTF-8
LABEL authors="Adam Frank <afrank@mozilla.com>"
ARG POETRY_HTTP_BASIC_PYPI_USERNAME
ARG POETRY_HTTP_BASIC_PYPI_PASSWORD
RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends \
    curl \
 && apt-get autoremove -y
RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  pkg-config \
  git-core
ENV POETRY_VERSION 1.0.9
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"
COPY . /workspace
WORKDIR /workspace
RUN python -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir -U 'pip<20' && \
  pip install --upgrade pip && \
  poetry install --no-dev --no-root --no-interaction && \
  poetry run tox && \
#  poetry config repositories.dp2 https://dp2-prod.appspot.com/pypi && \
#  poetry publish --build -r dp2 --username=$POETRY_HTTP_BASIC_PYPI_USERNAME --password=$POETRY_HTTP_BASIC_PYPI_PASSWORD && \
  pip install --no-deps dist/*.whl && \
  rm -rf dist *.egg-info
