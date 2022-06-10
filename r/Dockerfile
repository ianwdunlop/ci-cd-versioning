FROM r-base

RUN apt-get update -yqq && apt-get install -yqq build-essential apt-transport-https ca-certificates curl gnupg git bc jq wget git-lfs python3 python3-pip r-cran-devtools pandoc qpdf
RUN git lfs install

WORKDIR /scripts
COPY cictl .
COPY lib ./lib
COPY r/*.sh .

ENV PATH $PATH:/scripts

CMD bash