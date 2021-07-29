#! /usr/bin/env python

import os

from git.cmd import Git
from git.exc import GitCommandError

def rebase(branch: str):
    git = Git(".")
    git.checkout(branch)
    git.rebase(os.getenv("CI_COMMIT_BRANCH"))
    git.push("origin", branch)

def get_rebase_branch() -> str:
    branch = os.getenv("REBASE_BRANCH")
    if branch:
        return branch
    
    git = Git(".")
    try:
        git.show_ref("--verify", "--quiet", "refs/remotes/origin/develop")
        return "develop"
    except GitCommandError:
        pass

    try:
        git.show_ref("--verify", "--quiet", "refs/remotes/origin/dev")
        return "dev"
    except GitCommandError:
        return None

if __name__ == "__main__":
    branch = get_rebase_branch()
    rebase(branch)