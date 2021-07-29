#! /usr/bin/env python

from argparse import ArgumentParser
from git.cmd import Git
import re

parser = ArgumentParser()
parser.add_argument('tag')
args = parser.parse_args()

major=r"breaking-change|major"
minor=r"feature|minor"

git = Git(".")
if args.tag == "none":
    commit_prefixes = re.sub(fr"\({major}\|{minor}\):.*", "\1", git.log("--no-merges", '--pretty=format:"%s"'))
    # branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into 'master'", "\1", git.log("--merges", "--oneline"))
else:
    commit_prefixes = re.sub(fr"\({major}\|{minor}\):.*", "\1", git.log("--no-merges", '--pretty=format:"%s"', f"{args.tag}..HEAD"))
    # branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into 'master'", r"\1", git.log("--merges", "--oneline", f"{args.tag}..HEAD"))

print(commit_prefixes)
# print(branch_prefixes)