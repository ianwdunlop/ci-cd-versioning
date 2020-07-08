#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/parse-common-flags.sh" "$@"
reportError $?

PREVIOUS_TAG="$("$DIR"/previous-tag.sh)"
reportError $?

BUMP="$("$DIR"/bump.sh "$PREVIOUS_TAG")"
reportError $?

GIT_LOG="$("$DIR"/git-log.sh "$PREVIOUS_TAG")"
reportError $?

export PREVIOUS_TAG
export BUMP
export GIT_LOG