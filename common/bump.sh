#!/bin/bash

if [ $# -ne 1 ]; then
  echo "usage: ./bump.sh [previous tag]" >&2
  exit 1
fi

breaking_change="breaking-change"
feature="feature"

if [[ $VERSIONING_STRATEGY == "commits" ]]; then
  if [[ $1 != "none" ]]; then
    commit_prefixes=$(git log --no-merges --pretty=format:"%s" "$1..HEAD" | sed -n "s/\(${breaking_change}\|${feature}\):.*/\1/p")
  else
    commit_prefixes=$(git log --no-merges --pretty=format:"%s" | sed -n "s/\(${breaking_change}\|${feature}\):.*/\1/p")
  fi

  if [[ $commit_prefixes =~ $breaking_change ]]; then
    echo "major"
  elif [[ $commit_prefixes =~ $feature ]]; then
    echo "minor"
  else
    echo "patch"
  fi

elif [[ $VERSIONING_STRATEGY == "branches" ]]; then
  if [[ $1 != "none" ]]; then
    branch_prefixes=$(git log --merges --oneline "$1..HEAD" | sed -n "s/.*Merge branch '\(${breaking_change}\|${feature}\)\/.*' into '\(develop\|master\)'/\1/p")
  else
    branch_prefixes=$(git log --merges --oneline | sed -n "s/.*Merge branch '\(${breaking_change}\|${feature}\)\/.*' into '\(develop\|master\)'/\1/p")
  fi

  if [[ $branch_prefixes =~ $breaking_change ]]; then
    echo "major"
  elif [[ $branch_prefixes =~ $feature ]]; then
    echo "minor"
  else
    echo "patch"
  fi

else
  echo "VERSIONING_STRATEGY environment variable must be set to 'branches' or 'commits'." >&2
  exit 1
fi