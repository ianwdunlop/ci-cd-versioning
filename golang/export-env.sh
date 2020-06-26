#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PREVIOUS_TAG="$("$DIR"/previous-tag.sh)"
BUMP="$("$DIR"/bump.sh "$PREVIOUS_TAG" --branches)"
RELEASE_TAG="$("$DIR"/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
GIT_LOG="$("$DIR"/git-log.sh "$PREVIOUS_TAG")"

export PREVIOUS_TAG
export BUMP
export RELEASE_TAG
export GIT_LOG
