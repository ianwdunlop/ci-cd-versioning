#!/bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./export-env.sh [--commits|--branches]"
  exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PREVIOUS_TAG="$("$DIR"/previous-tag.sh)"
BUMP="$("$DIR"/bump.sh "$PREVIOUS_TAG" "$1")"
RELEASE_TAG="$("$DIR"/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
RELEASE_VERSION="$("$DIR"/next-tag.sh "$PREVIOUS_TAG" "$BUMP" --no-prefix)"
GIT_LOG="$("$DIR"/git-log.sh "$PREVIOUS_TAG")"
NEXT_VERSION="$("$DIR"/next-tag.sh "$RELEASE_TAG" patch --no-prefix)a0"

export PREVIOUS_TAG
export BUMP
export RELEASE_TAG
export RELEASE_VERSION
export GIT_LOG
export NEXT_VERSION
