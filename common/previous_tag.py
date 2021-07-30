#! /usr/bin/env python

from git.cmd import Git
from git.exc import GitCommandError

def previous_tag() -> str:
    git = Git(".")
    try:
        return git.describe("--abbrev=0")
    except GitCommandError:
        return "none"

if __name__ == "__main__":
    print(previous_tag)
