#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

if [ $# -lt 2 ]; then
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]" >&2
  exit 1
fi

tag=$1
major=0
minor=0
patch=0
prefix=""

regex="v.+"
if [[ $tag =~ $regex ]]; then
  prefix="v"
fi

regex="([0-9]+)\.([0-9]+)\.([0-9]+)"
if [[ $tag =~ $regex ]]; then
  major="${BASH_REMATCH[1]}"
  minor="${BASH_REMATCH[2]}"
  patch="${BASH_REMATCH[3]}"
elif [[ $tag == "none" ]] && [[ $3 == "--no-prefix" ]]; then
  echo "0.0.1"
  exit 0
elif [[ $tag == "none" ]]; then
  echo "v0.0.1"
  exit 0
else
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]" >&2
  echo "[previous tag] must be semver or 'none'"
  exit 1
fi

if [[ "$2" == "major" ]]; then
  major=$(echo $major + 1 | bc)
  reportError $?
  minor=0
  patch=0
elif [[ "$2" == "minor" ]]; then
  minor=$(echo $minor + 1 | bc)
  reportError $?
  patch=0
elif [[ "$2" == "patch" ]]; then
  patch=$(echo $patch + 1 | bc)
else
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]" >&2
  exit 1
fi

if [[ $3 == "--no-prefix" ]]; then
  echo "${major}.${minor}.${patch}"
else
  echo "${prefix}${major}.${minor}.${patch}"
fi
