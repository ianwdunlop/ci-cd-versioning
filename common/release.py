#! /usr/bin/env python

from setup_git import setup_git
from export_env import export_env
from version import version
from create_release import create_release
from rebase import rebase
import os

ci_user = os.getenv("CI_USER")
ci_user_email = os.getenv("CI_USER_EMAIL")

ci_token = os.getenv('CI_TOKEN')
if not ci_token:
    raise EnvironmentError("Missing environment variable CI_TOKEN")

setup_git(ci_token, ci_user=ci_user, ci_user_email=ci_user_email)
export_env()
version(os.getenv("RELEASE_TAG"))
create_release(os.getenv("RELEASE_TAG"), os.getenv("GIT_LOG"), os.getenv("CI_TOKEN"))
rebase()