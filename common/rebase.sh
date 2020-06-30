#! /bin/bash

if [ -z "$REBASE_BRANCH" ]; then
    echo "No rebase branch configured. Skipping..." >&2
    exit 0
fi

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

if git checkout "$REBASE_BRANCH" &> /dev/null; then
    echo "Checked out $REBASE_BRANCH..."
else 
    echo "Warning, rebase failed. Couldn't check out $REBASE_BRANCH. Exiting..." >&2
    exit 0
fi

if git pull &> /dev/null; then
    echo "Pulled changes to $REBASE_BRANCH..."
else 
    echo "Warning, rebase failed. Couldn't pull changes to $REBASE_BRANCH. Exiting..." >&2
    exit 0
fi

if git rebase "$CI_COMMIT_BRANCH" &> /dev/null; then
    echo "Rebased $REBASE_BRANCH onto $CI_COMMIT_BRANCH..."
else 
    echo "Warning, rebase failed. Couldn't rebase $REBASE_BRANCH onto $CI_COMMIT_BRANCH. Exiting..." >&2
    exit 0
fi

if git push origin "$REBASE_BRANCH" &> /dev/null; then 
    echo "Pushed changes successfully"
else 
    echo "Warning, rebase failed. Couldn't push changes to $REBASE_BRANCH. Exiting..." >&2
    exit 0
fi
