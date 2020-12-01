#! /bin/bash

if [ -z "$REBASE_BRANCH" ]; then
    echo "No rebase branch configured. Skipping..." >&2
    exit 0
fi

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

echo "Checking out $REBASE_BRANCH..."
git checkout "$REBASE_BRANCH"

echo "Rebasing $REBASE_BRANCH onto $CI_COMMIT_BRANCH..."
git rebase "$CI_COMMIT_BRANCH"

echo "Pushing changes to $REBASE_BRANCH..."
git push origin "$REBASE_BRANCH"
