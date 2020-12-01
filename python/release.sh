#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./release.sh [source module]"
  exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/utils.sh"

# shellcheck source=.
. "$DIR/setup-git.sh"
reportError $?

# shellcheck source=.
. "$DIR/export-env.sh" "$@"
reportError $?

# shellcheck source=.
. "$DIR/version.sh"
reportError $?

# shellcheck source=.
. "$DIR/create-release.sh"
reportError $?

# shellcheck source=.
. "$DIR/rebase.sh"
reportError $?