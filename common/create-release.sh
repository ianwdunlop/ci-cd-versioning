#! /bin/bash

curl --header 'Content-Type: application/json' \
      --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN" \
      --data "{ \"name\": \"$RELEASE_TAG\", \"tag_name\": \"$RELEASE_TAG\", \"description\": \"## Changelog\n\n$GIT_LOG\" }" \
      --request POST "https://gitlab.mdcatapult.io/api/v4/projects/$CI_PROJECT_ID/releases"