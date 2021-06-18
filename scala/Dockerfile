ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/scala:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

WORKDIR /scripts
ENV PATH $PATH:/scripts

COPY common/*.sh /scripts/
COPY scala/*.sh /scripts/

CMD bash
