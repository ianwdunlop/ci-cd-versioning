FROM registry.mdcatapult.io/informatics/docker-images/ci:common

ENV GOVERSION 1.14.4

RUN curl -O -J https://dl.google.com/go/go$GOVERSION.linux-amd64.tar.gz && \
        tar -C /usr/local -xzf go$GOVERSION.linux-amd64.tar.gz

ENV PATH $PATH:/usr/local/go/bin
ENV GOPATH /go
ENV PATH $PATH:$GOPATH/bin
ENV CGO_ENABLED 0

RUN curl -sfL https://install.goreleaser.com/github.com/goreleaser/goreleaser.sh | sh
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.28.0
RUN go get -u golang.org/x/tools/...

COPY golang/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']
