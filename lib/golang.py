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

import os
from lib.common import (
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    REBASE_BRANCH,
    ci_server_host,
    ci_server_port,
    create_release,
    env as common_env,
    ci_readonly_token,
    ci_readonly_user,
    rebase,
    set_git_config,
    fetch_all_and_checkout_latest,
    create_attachment,
    version
)

GOPRIVATE = "GOPRIVATE"


def netrc_file():
    return f"\nmachine {ci_server_host()}\n\tlogin {ci_readonly_user()}\n\tpassword {ci_readonly_token()}"


def config_goprivate():
    with open(f"{os.getenv('HOME')}/.netrc", 'a') as netrc:
        netrc.write(netrc_file())
    print(f"export GOPRIVATE={ci_server_host()}:{ci_server_port()}/*")

def env(args: list) -> dict:
    e = common_env(args)
    # Golang requires that semver versions are prefixed with "v".
    # There is an open issue for this https://github.com/golang/go/issues/32945.
    # Here we're just getting the value from the dict returned by 'env' and 
    # prefixing it. Then overriding it in the returned dictionary.
    tag = "v" + e[NEXT_TAG]
    e[NEXT_TAG] = tag
    e[GOPRIVATE] = f"{ci_server_host()}:{ci_server_port()}/*"
    return e


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
