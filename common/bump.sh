#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./bump.sh [previous tag] [--commits|--branches]"
  exit 1
fi

breaking_change="breaking-change"
feature="feature"

if [[ $2 == "--commits" ]]; then
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

elif [[ $2 == "--branches" ]]; then
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
  echo "usage: ./bump.sh [previous tag] [--commits|--branches]"
  exit 1
fi