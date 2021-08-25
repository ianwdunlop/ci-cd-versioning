ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/python:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN pip install pipenv
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /scripts
COPY cictl .
COPY lib ./lib

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash

