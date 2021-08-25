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
    config_git,
    create_attachment,
    git
)


def release(args: list):
    config_git()
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
    # The following npm command is behaving very strangely. 
    # It is supposed to commit the updated package.json and then
    # tag that commit with the new version. It does this fine when 
    # invoked with bash. When invoked with python, it seems to only 
    # update the package.json file. This is why there are additional 
    # commit and push commands below.
    check_call(["npm", "version", tag, "-m", "Setting version to %s"])
    
    # NOTE: The git commit command will fail if the commit is empty,
    # meaning that if this npm behaviour is fixed, this function will break.
    # In this event, just remove the commit and tag commands.
    git.commit("-am", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
