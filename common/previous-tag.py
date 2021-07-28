#! /usr/bin/env python

from git.repo.base import Repo

try:
    print(Repo().tags[-1].name)
except IndexError:
    print("none")

