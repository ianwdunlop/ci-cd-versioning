#! /bin/bash

if [ $# -lt 1 ]; then
  echo "usage: ./write-version.sh [version]"
  exit 1
fi

version=$1
file="$VERSION_DIR/version.py"
hash=$(git rev-parse --short HEAD)

if test -f "${file}"; then
  sed -i "/\(__version__\|__hash__\)/d" "${file}"
  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" >> "${file}"
else
  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" > "${file}"
fi
