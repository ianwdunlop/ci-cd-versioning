#  Copyright 2024 Medicines Discovery Catapult
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
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
    UPLOADS,
    short_sha,
    create_attachment,
    ci_commit_branch,
    package_password,
    pypi_username,
    pypi_password,
    pypi_host,
    git
)

development_version_tag = "a0"

# If using a custom repo then create a pip conf file
def config_pip():
    index_path = "repository/pypi-all/pypi"
    index_url_path = "repository/pypi-all/simple"
    if package_password():
        check_call(["pip", "config", "set", "global.index",
                    f"https://{pypi_username()}:{pypi_password()}@{pypi_host()}/{index_path}"])
        check_call(["pip", "config", "set", "global.index-url",
                    f"https://{pypi_username()}:{pypi_password()}@{pypi_host()}/{index_url_path}"])
        check_call(['pip', 'config', 'set', 'global.trusted-host', f'{pypi_host()}'])


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


def write_version(tag: str, version_dir: str):
    with open(_version_file(version_dir), "w") as f:
        f.writelines([f"__version__ = \"{tag}\"\n", f"__hash__ = \"{short_sha()}\"\n"])


def _version_file(version_dir: str) -> str:
    return f"{version_dir}/version.py"
