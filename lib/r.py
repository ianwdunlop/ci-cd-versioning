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
import shutil

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
    version_text = f'Setting version to {tag}'
    git.add(_version_file(version_dir))
    git.commit("-m", version_text)
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", version_text)
    # git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
    write_version(next_version, version_dir)
    next_version_text = f'Setting version to {next_version}'
    git.commit("-am", next_version_text)
    # git.commit("-am", f'Setting version to {next_version}')
    git.push("origin", ci_commit_branch())


# Write a tag, ie semantic version eg 1.2.3, out to the DESCRIPTION file
# It could be a release version eg 2.3.4 or a development version eg 2.3.5a0
def write_version(tag: str, version_dir: str):
    with open(_version_file(version_dir)) as f_in, open(f"{version_dir}/DESCRIPTION2", 'w') as f_out:
        for line in f_in:
            if line.startswith("Version:"):
                f_out.write(f"Version: {tag}\n")
            else:
                f_out.write(line)
    shutil.move(f"{version_dir}/DESCRIPTION2", _version_file(version_dir))


def _version_file(version_dir: str) -> str:
    return f"{version_dir}/DESCRIPTION"
