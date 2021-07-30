from lib.common import (
    BUMP,
    RELEASE_TAG,
    UPLOADS, 
    ci_commit_branch,
    create_release,
    export_env,
    rebase,
    setup_git,
    upload_files

)
from subprocess import call
from git.cmd import Git
import os

def release():
    setup_git()
    export_env()
    tag = os.getenv(RELEASE_TAG)
    uploads = os.getenv(UPLOADS)
    version()
    create_release(tag)
    upload_files(uploads, tag)
    rebase()

def version():
    git = Git(".")
    call("npm", "version", os.getenv(BUMP), "-m", "Setting version to v%s")
    git.push("origin", ci_commit_branch)
    git.push("origin", "--tags")