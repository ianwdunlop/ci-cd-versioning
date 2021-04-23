ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/python:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN pip config set global.trusted-host "nexus.wopr.inf.mdc pypi.org files.pythonhosted.org"
RUN pip install wheel twine pipenv

COPY common/*.sh /scripts/
COPY python/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash

