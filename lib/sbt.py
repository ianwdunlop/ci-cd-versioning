from subprocess import check_call
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
    check_call(["sbt", f'release with-defaults release-version {tag} next-version {next_version}'])


def release(args: list):
    config_git()
    e = env(args)

    # next_version has no "v" prefix
    next_version = e[NEXT_TAG]

    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    snapshot = next_tag(next_version, "patch") + "-SNAPSHOT"
    version(next_version, snapshot)

    # sbt-release auto adds the v prefix to git tags, so calls to gitlab
    # need to add it back in.
    next_git_tag = f"v{next_version}"
    create_release(next_git_tag, log)
    create_attachment(uploads, next_git_tag)
    rebase(rebase_branch)
