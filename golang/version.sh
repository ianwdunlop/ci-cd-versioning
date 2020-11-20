#! /bin/bash

git commit --allow-empty -am "Setting version to ${RELEASE_TAG}"
git push origin "$CI_COMMIT_BRANCH"
git tag -a "${RELEASE_TAG}" -m "Setting version to ${RELEASE_TAG}"
git push origin --tags
