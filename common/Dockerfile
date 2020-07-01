FROM ubuntu:18.04

RUN apt-get update -yqq && apt-get install -yqq apt-transport-https ca-certificates curl gnupg git bc

COPY common/*.sh /scripts/

CMD ['/bin/bash']
