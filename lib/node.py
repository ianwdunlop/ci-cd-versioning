from lib.common import (
    BUMP,
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    REBASE_BRANCH,
    ci_commit_branch,
    create_release,
    env,
    rebase,
    config_git,
    create_attachment,
    git
)
from subprocess import call


def release(args: list):
    config_git()
    e = env(args)
    bump = e[BUMP]
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    version(bump)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)


def version(bump: str):
    call(["npm", "version", bump, "-m", "Setting version to v%s"])
    git.push("origin", ci_commit_branch())
    git.push("origin", "--tags")
