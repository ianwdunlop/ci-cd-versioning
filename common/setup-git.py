#! /usr/bin/env python

import os

from git.cmd import Git

def setup_git(ci_token, ci_user=None, ci_user_email=None):
    if not ci_user:
        ci_user=f"project_{os.getenv('CI_PROJECT_ID')}_bot"
    
    if not ci_user_email:
        ci_user_email=f"project{os.getenv('CI_PROJECT_ID')}_bot@example.com"

    git = Git(".")
    host = os.getenv("CI_SERVER_HOST")
    path = os.getenv("CI_PROJECT_PATH")
    git.remote("set-url", "origin", f"https://{ci_user}:{ci_token}@{host}/{path}.git")
    git.config("user.name", ci_user)
    git.config("user.email", ci_user_email)
    git.fetch("--all", "--tags")
    git.checkout(os.getenv("CI_COMMIT_BRANCH"))
    git.pull("origin", os.getenv("CI_COMMIT_BRANCH"))

if __name__ == "__main__":
    ci_user = os.getenv("CI_USER")
    ci_user_email = os.getenv("CI_USER_EMAIL")
    
    ci_token = os.getenv('CI_TOKEN')
    if not ci_token:
        raise EnvironmentError("Missing environment variable CI_TOKEN")
    
    setup_git(ci_token, ci_user=ci_user, ci_user_email=ci_user_email)