#! /bin/bash

command -v ssh-agent || ( apt-get install -qq openssh-client )
eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -
mkdir -p ~/.ssh
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
git remote set-url origin "git@gitlab.mdcatapult.io:$CI_PROJECT_PATH.git"
git config --global user.email "$GIT_RELEASE_EMAIL"
git config --global user.name "$GIT_RELEASE_USER"

git fetch --all --tags
git checkout "$CI_COMMIT_BRANCH"
git pull origin "$CI_COMMIT_BRANCH"
