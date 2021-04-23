ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/node:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN apt-get install -yqq chromium
ENV CHROME_BIN=/usr/bin/chromium

COPY certs /certs
COPY common/*.sh /scripts/
COPY node/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

COPY /certs/* /usr/local/share/ca-certificates
RUN update-ca-certificates

CMD bash