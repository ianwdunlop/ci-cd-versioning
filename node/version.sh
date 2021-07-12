#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

RELEASE_TAG=$(npm version "${BUMP}" -m "Setting version to v%s")
reportError $?

git push origin "${CI_COMMIT_BRANCH}"
reportError $?

git push origin --tags
reportError $?

export RELEASE_TAG
