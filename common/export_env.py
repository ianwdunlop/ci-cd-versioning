#! /usr/bin/env python

import os

from parse_common_flags import parse_common_flags
from previous_tag import previous_tag
from bump import bump
from next_tag import next_tag
from git_log import git_log

def export_env() -> dict:
    env = parse_common_flags()

    tag = previous_tag()
    env["PREVIOUS_TAG"] = tag

    bump_amount = bump(tag)
    env["BUMP"] = bump_amount

    release_tag = next_tag(tag, bump_amount)
    env["RELEASE_TAG"] = release_tag

    log = git_log(tag)
    env["GIT_LOG"] = log

    for key, value in env.items():
        os.environ[key] = value

    return env

if __name__ == "__main__":
    for key, value in export_env().items():
        print(f"{key}={value}")