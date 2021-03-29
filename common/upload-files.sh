#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

if [ $# -lt 2 ]; then
  echo "usage: ./upload-files.sh [glob pattern] [tag name]" >&2
  exit 1
fi

for FILE in $1; do
  LINK="https://$CI_SERVER_HOST$(curl --request POST --header "PRIVATE-TOKEN: $CI_TOKEN" \
      --form "file=@$FILE" "$CI_API_V4_URL/projects/$CI_PROJECT_ID/uploads" | jq -r '.full_path')"
  reportError $?

  curl --request POST --header "PRIVATE-TOKEN: $CI_TOKEN" \
       --data name="$(basename "$FILE")" --data url="$LINK" \
       "$CI_API_V4_URL/projects/$CI_PROJECT_ID/releases/$2/assets/links"
  reportError $?
done
