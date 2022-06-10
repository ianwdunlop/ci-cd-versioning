import argparse
import re
from pathlib import Path
from subprocess import check_call
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
    LATEST_TAG,
    UPLOADS,
    short_sha,
    create_attachment,
    ci_commit_branch,
    nexus_username,
    nexus_password,
    nexus_host,
    git
)


# def config_r():
#     index_path = "repository/r-hosted"
#     index_url_path = "repository/pypi-all/simple"
#     check_call(["pip", "config", "set", "global.index",
#                 f"https://{nexus_username()}:{nexus_password()}@{nexus_host()}/{index_path}"])
#     check_call(["pip", "config", "set", "global.index-url",
#                 f"https://{nexus_username()}:{nexus_password()}@{nexus_host()}/{index_url_path}"])
#     check_call(['pip', 'config', 'set', 'global.trusted-host', f'{nexus_host()}'])


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
    current_tag = e[LATEST_TAG]
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    next_version = next_tag(tag, "patch") + "a0"
    version(tag, next_version, version_dir)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)


def version(new_tag: str, next_version: str, version_dir: str):
    write_version(new_tag, version_dir)
    git.add(_version_file(version_dir))
    git.commit("-m", f'Setting version to {new_tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", new_tag, "-m", f'Setting version to {new_tag}')
    git.push("origin", "--tags")
    write_version(next_version, version_dir)
    git.commit("-am", f'Setting version to {next_version}')
    git.push("origin", ci_commit_branch())


# Write the latest tag ie semantic version tag out to the DESCRIPTION file
# development_version is the next dev tag eg 1.2.3a0.
def write_version(development_version: str, version_dir: str):
    with open(_version_file(version_dir), "r") as f:
        content = f.read()
        version_regex = '(Version *.*)'
        replaced_content = re.sub(version_regex, f'Version: {development_version}', content, re.M)
    with open(_version_file(version_dir), "w") as f:
        f.write(replaced_content)


def _version_file(version_dir: str) -> str:
    return f"{version_dir}/DESCRIPTION"
