#! /bin/bash

if [ $# -lt 2 ]; then
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]"
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
  echo "1.0.0"
  exit 0
elif [[ $tag == "none" ]]; then
  echo "v1.0.0"
  exit 0
else
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]"
  echo "[previous tag] must be semver or 'none'"
  exit 1
fi

if [[ "$2" == "major" ]]; then
  major=$(echo $major + 1 | bc)
  minor=0
  patch=0
elif [[ "$2" == "minor" ]]; then
  minor=$(echo $minor + 1 | bc)
  patch=0
elif [[ "$2" == "patch" ]]; then
  patch=$(echo $patch + 1 | bc)
else
  echo "usage: ./next-tag.sh [previous tag] [major|minor|patch]"
  exit 1
fi

if [[ $3 == "--no-prefix" ]]; then
  echo "${major}.${minor}.${patch}"
else
  echo "${prefix}${major}.${minor}.${patch}"
fi
