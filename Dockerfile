FROM python:3
LABEL authors="Adam Frank <afrank@mozilla.com>"
COPY . /workspace
WORKDIR /workspace
RUN pip3 install poetry \
    && poetry install \
    && poetry build \
    && poetry run tox
