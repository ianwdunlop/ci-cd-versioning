#! /bin/bash

if [ $# -lt 2 ]; then
  echo "usage: ./upload-files.sh [glob pattern] [tag name]" >&2
  exit 1
fi

for FILE in $1; do
  LINK="https://gitlab.mdcatapult.io$(curl --request POST --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN" \
      --form "file=@$FILE" "https://gitlab.mdcatapult.io/api/v4/projects/$CI_PROJECT_ID/uploads" | jq -r '.full_path')"
  reportError $?

  curl --request POST --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN" \
       --data name="$(basename "$FILE")" --data url="$LINK" \
       "https://gitlab.mdcatapult.io/api/v4/projects/$CI_PROJECT_ID/releases/$2/  assets/links"
done
