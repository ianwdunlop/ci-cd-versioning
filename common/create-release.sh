#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

"${DIR}/create-release.py"
reportError $?

if ! [ -z "$UPLOADS" ]; then
  # shellcheck source=.
  . "${DIR}/upload-files.sh" "${UPLOADS}" "${RELEASE_TAG}"
  reportError $?
fi
