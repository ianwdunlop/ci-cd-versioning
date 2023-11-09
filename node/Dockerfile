ARG TAG=16.14.2-buster
FROM node:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

COPY certificates /certs
RUN cp /certs/*.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

RUN apt-get install -yqq chromium
ENV CHROME_BIN=/usr/bin/chromium

WORKDIR /scripts

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cictl .
COPY lib ./lib
COPY node/*.sh .

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash
