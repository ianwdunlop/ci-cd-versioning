ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/node:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs chromium
RUN git lfs install

ENV CHROME_BIN=/usr/bin/chromium

COPY common/*.sh /scripts/
COPY node/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash
