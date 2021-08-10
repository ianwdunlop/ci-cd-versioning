from lib.common import (
    BUMP,
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    ci_commit_branch,
    create_release,
    env,
    rebase,
    config_git,
    create_attachment

)
from subprocess import call
from git.cmd import Git
import os


def release():
    config_git()
    e = env()
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    version()
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase()


def version():
    git = Git(".")
    call(["npm", "version", os.getenv(BUMP), "-m", "Setting version to v%s"])
    git.push("origin", ci_commit_branch)
    git.push("origin", "--tags")
