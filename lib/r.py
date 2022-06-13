import argparse
import re

from lib.common import (
    GIT_LOG,
    REBASE_BRANCH,
    create_release,
    env,
    next_tag,
    rebase,
    set_git_config,
    fetch_all_and_checkout_latest,
    NEXT_TAG,
    UPLOADS,
    create_attachment,
    ci_commit_branch,
    git
)

development_version_tag = ".9000"


def release(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?")
    a, _ = parser.parse_known_args(args)
    version_dir = "src"
    if a.dir:
        version_dir = a.dir
    set_git_config()
    fetch_all_and_checkout_latest()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    next_version = next_tag(tag, "patch") + development_version_tag
    version(tag, next_version, version_dir)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)


def version(tag: str, next_version: str, version_dir: str):
    write_version(tag, version_dir)
    git.add(_version_file(version_dir))
    git.commit("-m", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
    write_version(next_version, version_dir)
    git.commit("-am", f'Setting version to {next_version}')
    git.push("origin", ci_commit_branch())


# Write a tag, ie semantic version eg 1.2.3, out to the DESCRIPTION file
# It could be a release version eg 2.3.4 or a development version eg 2.3.5a0
def write_version(tag: str, version_dir: str):
    with open(_version_file(version_dir), "r") as f:
        content = f.read()
        version_regex = '(Version: *.*)'
        replaced_content = re.sub(version_regex, f'Version: {tag}', content, re.M)
    with open(_version_file(version_dir), "w") as f:
        f.write(replaced_content)


def _version_file(version_dir: str) -> str:
    return f"{version_dir}/DESCRIPTION"
