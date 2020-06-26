#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./git-log.sh [previous tag]"
  exit 1
fi

if [[ $1 == "none" ]]; then
  git log --oneline --no-merges | awk -v ORS='  \\n' '1'
else
  git log --oneline --no-merges "$1..HEAD" | awk -v ORS='  \\n' '1'
fi

