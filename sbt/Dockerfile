ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/scala:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

WORKDIR /scripts

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cictl .
COPY lib ./lib

ENV PATH $PATH:/scripts

CMD bash
