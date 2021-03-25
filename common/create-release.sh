#! /bin/bash

if ! [[ $NO_RELEASE == "true" ]]; then
  curl --header 'Content-Type: application/json' \
      --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN" \
      --data "{ \"name\": \"$RELEASE_TAG\", \"tag_name\": \"$RELEASE_TAG\", \"description\": \"## Changelog\n\n$GIT_LOG\" }" \
      --request POST "$CI_API_V4_URL/projects/$CI_PROJECT_ID/releases"
  reportError $?  
fi


if ! [ -z "$UPLOADS" ]; then
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

  # shellcheck source=.
  . "$DIR/upload-files.sh" "$UPLOADS" "$RELEASE_TAG"
fi

