#! /usr/bin/env python
import argparse
import sys
parser = argparse.ArgumentParser()

# Optionals
parser.add_argument('--rebase', '-r')
parser.add_argument('--uploads', '-u')

# Flags
parser.add_argument('--no-release', '-N', action='store_true')
parser.add_argument('--commits', '-c', action='store_true')
parser.add_argument('--branches', '-b', action='store_true')

args = parser.parse_args()

if args.commits:
    print("Warn: Versioning strategy flags are now deprecated. Both commit message and branch prefixes can be used.", file=sys.stderr)

if args.branches:
    print("Warn: Versioning strategy flags are now deprecated. Both commit message and branch prefixes can be used.", file=sys.stderr)

if args.no_release:
    print("NO_RELEASE=true")
else:
    print("NO_RELEASE=false")

if args.rebase:
    print(f"REBASE_BRANCH={args.rebase}")

if args.uploads:
    print(f"UPLOADS={args.uploads}")