ARG TAG=latest
FROM registry.mdcatapult.io/informatics/docker-images/runners/golang:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip python3-venv
RUN git lfs install

WORKDIR /scripts

RUN curl -sfL https://install.goreleaser.com/github.com/goreleaser/goreleaser.sh | sh
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.38.0
RUN go get -u golang.org/x/tools/...

COPY requirements.txt .
RUN python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

COPY cictl .
COPY lib ./lib
COPY golang/*.sh .

ENV PATH $PATH:/scripts

CMD . venv/bin/activate && bash
