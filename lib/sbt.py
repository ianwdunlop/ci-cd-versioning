from subprocess import call
from lib.common import (GIT_LOG,
                        NEXT_TAG,
                        UPLOADS,
                        REBASE_BRANCH,
                        config_git,
                        create_attachment,
                        create_release,
                        env,
                        next_tag,
                        rebase)


def version(tag: str, next_version: str):
    call(["sbt", f'"release with-defaults release-version {tag} next-version {next_version}"'])


def release(args: list):
    config_git()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    snapshot = next_tag(tag, "patch") + "-SNAPSHOT"
    version(tag, snapshot)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)
