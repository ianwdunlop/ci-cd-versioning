FROM registry.mdcatapult.io/informatics/docker-images/ci:common-develop

ENV GOVERSION 1.14.4

RUN curl -sfL https://install.goreleaser.com/github.com/goreleaser/goreleaser.sh | sh

RUN curl -O -J https://dl.google.com/go/go$GOVERSION.linux-amd64.tar.gz && \
        tar -C /usr/local -xzf go$GOVERSION.linux-amd64.tar.gz

ENV PATH $PATH:/usr/local/go/bin
ENV GOPATH /go
ENV PATH $PATH:$GOPATH/bin

COPY golang/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']