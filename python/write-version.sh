#! /bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# shellcheck source=.
. "$DIR/utils.sh"

if [ $# -lt 1 ]; then
  echo "usage: ./write-version.sh [version]"
  exit 1
fi

version=$1
file="$VERSION_DIR/version.py"
hash=$(git rev-parse --short HEAD)
reportError $?

if test -f "${file}"; then
  sed -i "/\(__version__\|__hash__\)/d" "${file}"
  reportError $?

  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" >> "${file}"
  reportError $?

else
  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" > "${file}"
  reportError $?

fi
