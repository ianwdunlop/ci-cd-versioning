#! /bin/bash

function rebase() {

    echo "Checking out $1..."
    git checkout "$1"

    echo "Rebasing $1 onto $CI_COMMIT_BRANCH..."
    git rebase "$CI_COMMIT_BRANCH"

    echo "Pushing changes to $1..."
    git push origin "$1"
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck source=.
. "$DIR/utils.sh"

if ! [ -z "$REBASE_BRANCH" ]; then
    rebase "$REBASE_BRANCH"
    reportError $?
elif git show-ref --verify --quiet refs/remotes/origin/develop &> /dev/null; then
    rebase "develop"
    reportError $?
elif git show-ref --verify --quiet refs/remotes/origin/dev &> /dev/null; then
    rebase "dev"
    reportError $?
else
    echo "No rebase branch. Skipping rebase..."
    exit 0
fi
