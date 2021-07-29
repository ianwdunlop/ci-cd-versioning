#! /usr/bin/env python

from git.cmd import Git
from git.exc import GitCommandError

git = Git(".")

try:
    print(git.describe("--abbrev=0"))
except GitCommandError:
    print("none")
