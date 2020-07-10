FROM registry.mdcatapult.io/informatics/docker-images/ci:common

ENV NODE_VERSION=v12.16.2

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -yqq xz-utils chromium-browser python g++ libssl-dev make
ENV CHROME_BIN=/usr/bin/chromium-browser

WORKDIR /tmp
RUN curl https://nodejs.org/dist/$NODE_VERSION/node-${NODE_VERSION}-linux-x64.tar.xz \
    -o node-${NODE_VERSION}-linux-x64.tar.xz && \
    tar -xf node-${NODE_VERSION}-linux-x64.tar.xz

ENV PATH=$PATH:/tmp/node-${NODE_VERSION}-linux-x64/bin

COPY node/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']