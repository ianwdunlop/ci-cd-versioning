ARG TAG=latest
FROM python:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN pip install wheel twine pipenv

COPY certs /certs
COPY common/*.sh /scripts/
COPY python/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

COPY /certs/bundle.pem /usr/local/share/ca-certificates
RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE /certs/bundle.pem
RUN pip config set global.trusted-host "nexus.wopr.inf.mdc pypi.org files.pythonhosted.org"
CMD bash

