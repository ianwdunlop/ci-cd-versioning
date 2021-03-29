#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

if [ $# -ne 1 ]; then
  echo "usage: ./bump.sh [previous tag]" >&2
  exit 1
fi

# Defines major and minor keywords.
major="breaking-change\|major"
minor="feature\|minor"

# Pull keywords out of git log.
if [[ $1 != "none" ]]; then
  commit_prefixes=$(git log --no-merges --pretty=format:"%s" "$1..HEAD" | sed -n "s/\(${major}\|${minor}\):.*/\1/p")
  reportError $?
else
  commit_prefixes=$(git log --no-merges --pretty=format:"%s" | sed -n "s/\(${major}\|${minor}\):.*/\1/p")
  reportError $?
fi

if [[ $1 != "none" ]]; then
  branch_prefixes=$(git log --merges --oneline "$1..HEAD" | sed -n "s/.*Merge branch '\(${major}\|${minor}\)\/.*' into '\(develop\|master\)'/\1/p")
else
  branch_prefixes=$(git log --merges --oneline | sed -n "s/.*Merge branch '\(${major}\|${minor}\)\/.*' into '\(develop\|master\)'/\1/p")
fi

# Strip escape character from 
major="${major//\\}"
minor="${minor//\\}"

if [[ $commit_prefixes =~ $major ]]; then
  echo "major"
elif [[ $branch_prefixes =~ $major ]]; then
  echo "major"
elif [[ $commit_prefixes =~ $minor ]]; then
  echo "minor"
elif [[ $branch_prefixes =~ $minor ]]; then
  echo "minor"
else
  echo "patch"
fi

