ARG TAG=buster
FROM openjdk:$TAG

RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list && \
        echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list && \
        curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add

RUN apt-get update --allow-releaseinfo-change -yqq && apt-get install -yqq sbt build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

COPY certificates /certs
RUN cp /certs/*.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

WORKDIR /scripts

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY cictl .
COPY lib ./lib
COPY sbt/*.sh .

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash
