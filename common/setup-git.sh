#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

command -v ssh-agent || ( apt-get install -qq openssh-client )
reportError $?

eval "$(ssh-agent -s)"
reportError $?

echo "${SSH_PRIVATE_KEY}" | ssh-add -
reportError $?

mkdir -p ~/.ssh
reportError $?

[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
reportError $?

git remote set-url origin "git@$CI_SERVER_HOST:$CI_PROJECT_PATH.git"
reportError $?

git config --global user.email "$GIT_RELEASE_EMAIL"
reportError $?

git config --global user.name "$GIT_RELEASE_USER"
reportError $?


git fetch --all --tags
reportError $?

git checkout "$CI_COMMIT_BRANCH"
reportError $?

git pull origin "$CI_COMMIT_BRANCH"
reportError $?

