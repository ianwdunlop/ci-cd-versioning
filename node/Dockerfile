ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/node:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install
RUN pip3 install requests

RUN apt-get install -yqq chromium
ENV CHROME_BIN=/usr/bin/chromium

COPY common/*.sh /scripts/
COPY common/*.py /scripts/
COPY node/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash