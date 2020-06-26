#! /bin/bash

if [ $# -lt 2 ]; then
  echo "usage: ./write-version-py.sh [version] [module source]"
  exit 1
fi

version=$1
file="$2/version.py"
hash=$(git rev-parse --short HEAD)

if test -f "${file}"; then
  sed -i "/\(__version__\|__hash__\)/d" "${file}"
  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" >>"${file}"
else
  echo -e "__version__ = '${version}'\n__hash__ = '${hash}'" >"${file}"
fi
