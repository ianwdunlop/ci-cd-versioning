#! /usr/bin/env python

import os
import sys

from git.cmd import Git
from git.exc import GitCommandError

def rebase(branch: str):
    git = Git(".")
    
    print(f"Checking out {branch}", file=sys.stderr)
    git.checkout(branch)
    
    ci_commit_branch = os.getenv("CI_COMMIT_BRANCH")
    print(f"Rebasing {branch} onto {ci_commit_branch}", file=sys.stderr)
    git.rebase(ci_commit_branch)
    
    print(f"Pushing changes to $1", file=sys.stderr)
    git.push("origin", branch)

def get_rebase_branch() -> str:
    git = Git(".")
    branches = ["develop", "dev"]
    for branch in branches:
        try:
            git.show_ref("--verify", "--quiet", f"refs/remotes/origin/{branch}")
            return branch
        except GitCommandError:
            pass
    return ""

if __name__ == "__main__":
    branch = os.getenv("REBASE_BRANCH")
    if branch:
        rebase(branch)
        exit(0)
    
    branch = get_rebase_branch()
    if branch:
        rebase(branch)
    else:
        print("No rebase branch, skipping...", file=sys.stderr)