ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/debian:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

COPY common/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash
