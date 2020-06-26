#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./version-go.sh [source module] [branch]"
  exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck source=.
. "$DIR/write-version.sh" "${RELEASE_VERSION}" "$1"

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

git add .
git commit -m "Setting version to ${RELEASE_VERSION}"
git push origin "$2"
git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
git push origin --tags

# shellcheck source=.
. "$DIR/write-version.sh" "${NEXT_VERSION}" "$1"
git commit -am "Setting version to ${NEXT_VERSION}"
git push origin "$2"
