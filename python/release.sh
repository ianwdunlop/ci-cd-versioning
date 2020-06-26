#!/bin/bash

if [ $# -lt 2 ]; then
  echo "usage: ./release.sh [source module] [--commits|--branches]"
  exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/setup-git.sh" "$CI_COMMIT_BRANCH"

# shellcheck source=.
. "$DIR/export-env.sh" "$2"

# shellcheck source=.
. "$DIR/version.sh" "$1" "$CI_COMMIT_BRANCH"

# shellcheck source=.
. "$DIR/create-release.sh"