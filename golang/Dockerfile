ARG TAG=1.18
FROM golang:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

WORKDIR /scripts

RUN echo 'deb [trusted=yes] https://repo.goreleaser.com/apt/ /' | tee /etc/apt/sources.list.d/goreleaser.list
RUN apt-get update -yqq && apt-get install goreleaser -yqq
#RUN curl -sfL https://install.goreleaser.com/github.com/goreleaser/goreleaser.sh | sh
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.46.2
RUN go install golang.org/x/tools/...@v0.2.0

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cictl .
COPY lib ./lib
COPY golang/*.sh .

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash
