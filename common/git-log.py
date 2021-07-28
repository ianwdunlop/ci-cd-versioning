#! /usr/bin/env python

from git.repo.base import Repo

repo = Repo()
last_tag = repo.tags[-1]
print(f"last_tag: {last_tag.reference}")

print(repo.active_branch.commit)