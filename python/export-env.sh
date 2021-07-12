#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "${DIR}/utils.sh"

# shellcheck source=.
. "${DIR}/parse-common-flags.sh" "$@"
reportError $?

PREVIOUS_TAG="$("${DIR}"/previous-tag.sh)"
reportError $?

BUMP="$("${DIR}"/bump.sh "${PREVIOUS_TAG}")"
reportError $?

RELEASE_TAG="$("${DIR}"/next-tag.sh "${PREVIOUS_TAG}" "${BUMP}")"
reportError $?

RELEASE_VERSION="$("${DIR}"/next-tag.sh "${PREVIOUS_TAG}" "${BUMP}" --no-prefix)"
reportError $?

GIT_LOG="$("${DIR}"/git-log.sh "${PREVIOUS_TAG}")"
reportError $?

NEXT_VERSION="$("${DIR}"/next-tag.sh "${RELEASE_TAG}" patch --no-prefix)a0"
reportError $?

VERSION_DIR="$(trim "${PARAMS}")"

export PREVIOUS_TAG
export BUMP
export RELEASE_TAG
export RELEASE_VERSION
export GIT_LOG
export NEXT_VERSION
export VERSION_DIR