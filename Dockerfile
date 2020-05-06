FROM python:3
LABEL maintainer="Bryan Sieber bsieber@mozilla.com"

COPY cloudalerts /workspace/cloudalerts
COPY tests /workspace/tests
COPY .secrets.baseline setup.py /workspace/

WORKDIR /workspace

RUN pip3 install --upgrade --no-cache-dir .

RUN behave tests/bdd
