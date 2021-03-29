#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

echo -e "machine $CI_SERVER_HOST\n\tlogin $GIT_RELEASE_USER\n\tpassword $GIT_RELEASE_TOKEN" > ~/.netrc
reportError $?

GOPRIVATE="$CI_SERVER_HOST:$CI_SERVER_PORT/*"
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

export GOPRIVATE