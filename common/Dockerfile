ARG TAG=latest
FROM debian:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

COPY common/*.sh /scripts/

COPY certs /certs
WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash
