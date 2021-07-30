#! /usr/bin/env python

import os

from git.cmd import Git

def version(tag: str):
    git = Git(".")

    git.commit("--allow-empty", "-am", f'"Setting version to {tag}"')
    git.push("origin", os.getenv("CI_COMMIT_BRANCH"))
    git.tag("-a", tag, "-m", f"Setting version to {tag}")
    git.push("origin", "--tags")

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("tag")
    args = parser.parse_args()

    version(args.tag)