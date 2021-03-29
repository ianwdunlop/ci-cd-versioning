#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

eval "$(ssh-agent -s)"
reportError $?

echo "${SSH_PRIVATE_KEY}" | ssh-add -
reportError $?

sbt "release with-defaults release-version $RELEASE_VERSION next-version $NEXT_VERSION"
reportError $?