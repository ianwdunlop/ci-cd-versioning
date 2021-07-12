#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "${DIR}/utils.sh"

sbt "release with-defaults release-version ${RELEASE_VERSION} next-version ${NEXT_VERSION}"
reportError $?
