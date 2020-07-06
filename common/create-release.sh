#! /bin/bash

curl --header 'Content-Type: application/json' \
    --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN" \
    --data "{ \"name\": \"$RELEASE_TAG\", \"tag_name\": \"$RELEASE_TAG\", \"description\": \"## Changelog\n\n$GIT_LOG\" }" \
    --request POST "https://gitlab.mdcatapult.io/api/v4/projects/$CI_PROJECT_ID/releases"
reportError $?

if [ -z "$UPLOADS" ]; then
  echo "No files to upload. Exiting..." >&2
  exit 0
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/upload-files.sh $UPLOADS $RELEASE_TAG"
