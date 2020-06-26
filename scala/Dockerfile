FROM registry.mdcatapult.io/informatics/software-engineering/ci:common

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -yqq openjdk-14-jdk

RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list && \
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823 && \
        apt-get update -yqq && \
        apt-get install -yqq sbt

RUN sbt sbtVersion

COPY scala/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']