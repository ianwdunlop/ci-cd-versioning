FROM ubuntu:18.04

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget

COPY common/*.sh /scripts/

CMD ['/bin/bash']
