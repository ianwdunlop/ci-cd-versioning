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

from subprocess import check_call
from lib.common import (GIT_LOG,
                        NEXT_TAG,
                        UPLOADS,
                        REBASE_BRANCH,
                        set_git_config,
                        fetch_all_and_checkout_latest,
                        create_attachment,
                        create_release,
                        env,
                        next_tag,
                        rebase)


def version(tag: str, next_version: str):
    check_call(["sbt", f'release with-defaults release-version {tag} next-version {next_version}'])


def release(args: list):
    set_git_config()
    fetch_all_and_checkout_latest()
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
