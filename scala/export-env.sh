#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PREVIOUS_TAG="$("$DIR"/previous-tag.sh)"
BUMP="$("$DIR"/bump.sh "$PREVIOUS_TAG" --branches)"
RELEASE_TAG="$("$DIR"/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
RELEASE_VERSION="$("$DIR"/next-tag.sh "$PREVIOUS_TAG" "$BUMP" --no-prefix)"
GIT_LOG="$("$DIR"/git-log.sh "$PREVIOUS_TAG")"
NEXT_VERSION="$("$DIR"/next-tag.sh "$RELEASE_TAG" patch --no-prefix)-SNAPSHOT"

export PREVIOUS_TAG
export BUMP
export RELEASE_TAG
export RELEASE_VERSION
export GIT_LOG
export NEXT_VERSION
