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

CMD bash

