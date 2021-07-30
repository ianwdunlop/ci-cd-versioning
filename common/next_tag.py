#! /usr/bin/env python

import semver

def next_tag(current_tag: str, bump: str) -> str:
    no_prefix = current_tag.lstrip("v")
    ver = semver.VersionInfo.parse(no_prefix)
    return str(ver.next_version(bump))

if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('tag')
    parser.add_argument('bump')
    args = parser.parse_args()

    print(next_tag(args.tag, args.bump))