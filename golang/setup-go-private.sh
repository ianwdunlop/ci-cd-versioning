#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

echo -e "machine ${CI_SERVER_HOST}\n\tlogin gitlab-ci-token\n\tpassword ${CI_JOB_TOKEN}" > ~/.netrc
reportError $?
GOPRIVATE="${CI_SERVER_HOST}:${CI_SERVER_PORT}/*"

export GOPRIVATE