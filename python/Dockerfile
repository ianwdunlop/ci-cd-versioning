FROM registry.mdcatapult.io/informatics/docker-images/ci:common

ENV PYTHON_VERSION=3.7.7

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -yqq --no-install-recommends make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
    xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
    tar -xf Python-$PYTHON_VERSION.tgz && \
    cd Python-$PYTHON_VERSION && \
    ./configure --enable-optimizations && \
    make install

RUN update-alternatives --install /usr/local/bin/python python /usr/local/bin/python3 1 && \
    update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3 1

COPY python/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']

