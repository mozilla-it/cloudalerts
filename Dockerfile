FROM python:3

COPY cloudalerts /workspace/cloudalerts
COPY tests /workspace/tests
COPY .secrets.baseline pyproject.toml README.md /workspace/

WORKDIR /workspace

RUN pip install .
RUN pip install tox
RUN tox