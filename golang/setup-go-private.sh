#!/bin/bash

echo -e "machine $CI_SERVER_HOST\n\tlogin $GIT_RELEASE_USER\n\tpassword $GIT_RELEASE_TOKEN" > ~/.netrc
GOPRIVATE="$CI_SERVER_HOST:$CI_SERVER_PORT/*"
command -v ssh-agent || ( apt-get install -qq openssh-client )
eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -
mkdir -p ~/.ssh
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

export GOPRIVATE