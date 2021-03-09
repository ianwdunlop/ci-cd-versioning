FROM ubuntu:18.04

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs

RUN git lfs install

COPY common/*.sh /scripts/

CMD ['/bin/bash']
