FROM python:3

COPY cloudalerts /workspace/cloudalerts
COPY tests /workspace/tests
COPY .secrets.baseline pyproject.toml README.md /workspace/

WORKDIR /workspace

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-ansi --no-root
RUN poetry run tox

RUN poetry build