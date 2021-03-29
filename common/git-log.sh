#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

if [ $# -lt 1 ]; then
  echo "usage: ./git-log.sh [previous tag]" >&2
  exit 1
fi

if [[ $1 == "none" ]]; then
  git log --oneline --no-merges | awk -v ORS='  \\n' '1'
  reportError $?
else
  git log --oneline --no-merges "$1..HEAD" | awk -v ORS='  \\n' '1'
  reportError $?
fi

