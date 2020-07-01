FROM registry.mdcatapult.io/informatics/docker-images/ci:common-develop

ENV NODE_VERSION=v12.16.2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -yqq --no-install-recommends xz-utils

WORKDIR /tmp
RUN curl https://nodejs.org/dist/$NODE_VERSION/node-${NODE_VERSION}-linux-x64.tar.xz \
    -o node-${NODE_VERSION}-linux-x64.tar.xz && \
    tar -xf node-${NODE_VERSION}-linux-x64.tar.xz

ENV PATH=$PATH:/tmp/node-${NODE_VERSION}-linux-x64/bin

RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install --fix-missing -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

ENV CHROME_BIN=/usr/bin/google-chrome

COPY node/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']