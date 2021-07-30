#! /usr/bin/env python

from git.cmd import Git
import re

def git_log(tag: str) -> str:
    git = Git(".")
    log = git.log("--oneline", "--no-merges", f"{tag}..HEAD")
    return repr(log).strip("'")

def sanitize(log: str) -> str:
    sanitized_log = re.sub('&', '&amp', log)
    sanitized_log = re.sub('<', '&lt', sanitized_log)
    sanitized_log = re.sub('"', '&quot', sanitized_log)
    return re.sub('>', '&gt', sanitized_log)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('tag')
    args = parser.parse_args()

    print(sanitize(git_log(args.tag)))