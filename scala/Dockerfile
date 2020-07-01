FROM registry.mdcatapult.io/informatics/docker-images/ci:common-develop

ENV JDK_VERSION=14.0.1

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -yqq --no-install-recommends xz-utils

WORKDIR /usr/java
RUN curl https://download.java.net/java/GA/jdk14.0.1/664493ef4a6946b186ff29eb326336a2/7/GPL/openjdk-${JDK_VERSION}_linux-x64_bin.tar.gz \
    -o /tmp/openjdk-${JDK_VERSION}_linux-x64_bin.tar.gz && \
    tar -zxvf /tmp/openjdk-${JDK_VERSION}_linux-x64_bin.tar.gz

ENV JAVA_HOME=/usr/java/jdk-${JDK_VERSION}
ENV JRE_HOME=$JAVA_HOME
ENV PATH=$PATH:$JAVA_HOME/bin

RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list && \
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823 && \
        apt-get update -yqq && \
        apt-get install -yqq sbt

RUN sbt sbtVersion

COPY scala/*.sh /scripts/

WORKDIR /scripts

CMD ['/bin/bash']