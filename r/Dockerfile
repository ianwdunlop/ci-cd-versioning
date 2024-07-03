ARG TAG=3.16
FROM bioconductor/bioconductor_docker:$TAG

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip
RUN git lfs install

COPY certificates /certs
RUN cp /certs/*.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /scripts
COPY cictl .
COPY lib ./lib
COPY r/*.sh .

ENV PATH $PATH:/scripts
ENV GIT_PYTHON_TRACE full

CMD bash
