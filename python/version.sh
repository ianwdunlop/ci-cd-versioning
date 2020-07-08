#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck source=.
. "$DIR/write-version.sh" "${RELEASE_VERSION}"

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

git add .
git commit -m "Setting version to ${RELEASE_VERSION}"
git push origin "$CI_COMMIT_BRANCH"
git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
git push origin --tags

# shellcheck source=.
. "$DIR/write-version.sh" "${NEXT_VERSION}"
git commit -am "Setting version to ${NEXT_VERSION}"
git push origin "$CI_COMMIT_BRANCH"
