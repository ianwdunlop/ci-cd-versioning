#! /bin/bash

echo -e "machine $CI_SERVER_HOST\n\tlogin $CI_READONLY_USER\n\tpassword $CI_READONLY_TOKEN" > ~/.netrc
GOPRIVATE="$CI_SERVER_HOST:$CI_SERVER_PORT/*"

export GOPRIVATE