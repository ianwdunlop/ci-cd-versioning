ARG TAG=buster
FROM openjdk:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs
RUN git lfs install

RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list && \
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823 && \
        apt-get update -yqq && \
        apt-get install -yqq sbt
RUN sbt sbtVersion


COPY common/*.sh /scripts/
COPY scala/*.sh /scripts/

WORKDIR /scripts
ENV PATH $PATH:/scripts

CMD bash