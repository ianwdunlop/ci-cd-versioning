#! /usr/bin/env python

from git.cmd import Git
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('tag')
args = parser.parse_args()

git = Git(".")
log = git.log("--oneline", "--no-merges", f"{args.tag}..HEAD")
print(repr(log).strip("'"))