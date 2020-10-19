#! /bin/bash

set -m

GO_MODULE=$(head -n 1 go.mod | cut -f 2 -d ' ')

godoc &
PID=$!

while ! curl --fail --silent "localhost:6060" 2>&1 >/dev/null; do
  sleep 0.1
done

sleep 1

wget    --recursive \
        --no-verbose \
        --convert-links \
        --page-requisites \
        --adjust-extension \
        --execute=robots=off \
        --include-directories="/lib,/pkg/$GO_MODULE,/src/$GO_MODULE" \
        --exclude-directories="*" \
        --directory-prefix="godoc" \
        --no-host-directories \
        "http://localhost:6060/pkg/$GO_MODULE/"

kill $PID