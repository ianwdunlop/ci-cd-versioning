#! /usr/bin/env python

from git.cmd import Git
import re


def bump(tag: str) -> str:
    major=r"breaking-change|major"
    minor=r"feature|minor"

    git = Git(".")
    if tag == "none":
        commit_prefixes = re.sub(fr"({major}|{minor}):.*", r"\1", git.log("--no-merges", '--pretty=format:"%s"'))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into 'master'", "\1", git.log("--merges", "--oneline"))
    else:
        commit_prefixes = re.sub(fr"\"({major}|{minor}):.*", r"\1", git.log("--no-merges", '--pretty=format:"%s"', f"{tag}..HEAD"))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into 'master'", r"\1", git.log("--merges", "--oneline", f"{tag}..HEAD"))

    if re.match(major, commit_prefixes) or re.match(major, branch_prefixes):
        return "major"
    elif re.match(minor, commit_prefixes) or re.match(minor, branch_prefixes):
        return "minor"
    else:
        return "patch"

if __name__ == "__main__":

    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('tag')
    args = parser.parse_args()
    
    print(bump(args.tag))