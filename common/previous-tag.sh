#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "${DIR}/utils.sh"

if git describe --abbrev=0 &> /dev/null; then
  git describe --abbrev=0
  reportError $?
else
  echo "none"
fi




