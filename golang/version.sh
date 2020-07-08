#!/bin/bash

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

git commit --allow-empty -am "Setting version to ${RELEASE_TAG}"
git push origin "$CI_COMMIT_BRANCH"
git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
git push origin --tags
