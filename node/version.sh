#! /bin/bash

RELEASE_TAG=$(npm version "$BUMP" -m "Setting version to v%s")
reportError $?

git push origin "$CI_COMMIT_BRANCH"
git push origin --tags

export RELEASE_TAG
