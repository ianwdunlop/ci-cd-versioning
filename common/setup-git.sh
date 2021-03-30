#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

if [ -z "$CI_USER" ]; then
    CI_USER="project_${CI_PROJECT_ID}_bot"
fi

if [ -z "$CI_USER_EMAIL"]; then
    CI_USER_EMAIL="project${CI_PROJECT_ID}_bot@example.com"
fi

git remote set-url origin "https://${CI_USER}:${CI_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git"
reportError $?

git config user.email "$CI_USER_EMAIL"
reportError $?

git config user.name "$CI_USER"
reportError $?

git fetch --all --tags
reportError $?

git checkout "$CI_COMMIT_BRANCH"
reportError $?

git pull origin "$CI_COMMIT_BRANCH"
reportError $?

