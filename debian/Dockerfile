ARG TAG=latest
FROM debian:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

WORKDIR /scripts

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cictl .
COPY lib ./lib
COPY debian/*.sh .

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash
