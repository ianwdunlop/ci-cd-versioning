ARG TAG=latest
FROM golang:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN curl -sfL https://install.goreleaser.com/github.com/goreleaser/goreleaser.sh | sh
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.38.0
RUN go get -u golang.org/x/tools/...

COPY certs /certs
COPY common/*.sh /scripts/
COPY golang/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

COPY /certs/bundle.pem /usr/local/share/ca-certificates
RUN update-ca-certificates

CMD bash
