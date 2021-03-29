#! /bin/bash
REBASE_BRANCH=""
PARAMS=""
UPLOADS=""
NO_RELEASE="false"
while (( "$#" )); do
  case "$1" in
    -c|--commits)
      echo "Warn: Versioning strategy flags are now deprecated. Both commit message and branch prefixes can be used."
      shift
      ;;
    -b|--branches)
      echo "Warn: Versioning strategy flags are now deprecated. Both commit message and branch prefixes can be used."
      shift
      ;;
    -N|--no-release)
      NO_RELEASE="true"
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
    -u|--uploads)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        UPLOADS=$2
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
export REBASE_BRANCH
export UPLOADS
export NO_RELEASE