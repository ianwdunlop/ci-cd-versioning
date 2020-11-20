#! /bin/bash

if [ -z "$CI_USER" ]; then
    CI_USER="project_${CI_PROJECT_ID}_bot"
fi

if [ -z "$CI_USER_EMAIL"]; then
    CI_USER_EMAIL="project${CI_PROJECT_ID}_bot@example.com"
fi

git remote set-url origin "https://${CI_USER}:${CI_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git"
git config user.email "$CI_USER_EMAIL"
git config user.name "$CI_USER"

git fetch --all --tags
git checkout "$CI_COMMIT_BRANCH"
git pull origin "$CI_COMMIT_BRANCH"
