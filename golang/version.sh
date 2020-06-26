#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./version-go.sh [branch]"
  exit 1
fi

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

git commit --allow-empty -am "Setting version to ${RELEASE_TAG}"
git push origin "$1"
git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
git push origin --tags
