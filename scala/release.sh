#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/setup-git.sh" "$CI_COMMIT_BRANCH"

# shellcheck source=.
. "$DIR/export-env.sh"

# shellcheck source=.
. "$DIR/version.sh"

# shellcheck source=.
. "$DIR/create-release.sh"