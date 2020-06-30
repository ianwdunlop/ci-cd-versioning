#!/bin/bash
VERSIONING_STRATEGY="commits"
REBASE_BRANCH=""
PARAMS=""
while (( "$#" )); do
  case "$1" in
    -c|--commits)
      shift
      ;;
    -b|--branches)
      VERSIONING_STRATEGY="branches"
      shift
      ;;
    -r|--rebase)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        REBASE_BRANCH=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing [rebase branch]" >&2
        exit 1
      fi
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

export PARAMS
export VERSIONING_STRATEGY
export REBASE_BRANCH