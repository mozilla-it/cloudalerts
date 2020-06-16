FROM python:3

COPY cloudalerts /workspace/cloudalerts
COPY tests /workspace/tests
COPY .secrets.baseline poetry.lock pyproject.toml README.md /workspace/

WORKDIR /workspace

RUN pip3 install poetry \
    && poetry install \
    && poetry build \
    && poetry run tox
