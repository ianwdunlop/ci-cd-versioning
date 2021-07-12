#! /bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=.
. "$DIR/utils.sh"

# shellcheck source=.
. "$DIR/write-version.sh" "${RELEASE_VERSION}"
reportError $?

git add .
reportError $?

git commit -m "Setting version to ${RELEASE_VERSION}"
reportError $?

git push origin "${CI_COMMIT_BRANCH}"
reportError $?

git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
reportError $?

git push origin --tags
reportError $?

# shellcheck source=.
. "$DIR/write-version.sh" "${NEXT_VERSION}"
reportError $?

git commit -am "Setting version to ${NEXT_VERSION}"
reportError $?

git push origin "${CI_COMMIT_BRANCH}"
reportError $?
