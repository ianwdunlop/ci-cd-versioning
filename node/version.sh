#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./version.sh [branch]"
  exit 1
fi

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

RELEASE_TAG=$(npm version "$BUMP" -m "Setting version to v%s")
git push origin "$1"
git push origin --tags

export RELEASE_TAG
