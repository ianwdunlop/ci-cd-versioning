from subprocess import check_call
from lib.common import (
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    REBASE_BRANCH,
    ci_commit_branch,
    create_release,
    env,
    rebase,
    set_git_config,
    fetch_all_and_checkout_latest,
    create_attachment,
    git
)


def release(args: list):
    set_git_config()
    fetch_all_and_checkout_latest()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    version(tag)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)


def version(tag: str):
    # Call with --no-git-tag-version then commit and tag manually
    # afterwards. Otherwise this will fail if the npm project is
    # located in a subfolder.
    check_call(["npm", "--no-git-tag-version", "version", tag])
    
    git.commit("-am", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
