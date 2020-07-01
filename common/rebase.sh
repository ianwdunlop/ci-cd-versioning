#! /bin/bash

function ignoreError() {
    if [ "$1" -ne 0 ]; then
        exit 0
    fi
}

if [ -z "$REBASE_BRANCH" ]; then
    echo "No rebase branch configured. Skipping..." >&2
    exit 0
fi

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

echo "Refreshing $REBASE_BRANCH from remote..."
git branch -D "$REBASE_BRANCH"
git fetch origin "$REBASE_BRANCH"
ignoreError $?

echo "Rebasing $REBASE_BRANCH onto $CI_COMMIT_BRANCH..."
git rebase "$CI_COMMIT_BRANCH"
ignoreError $?

echo "Pushing changes to $REBASE_BRANCH..."
git push origin "$REBASE_BRANCH"
ignoreError $?
