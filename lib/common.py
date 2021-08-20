import re
import os
import sys
import argparse
import glob
import json
import semver
import requests
from requests.models import HTTPError
from git.cmd import Git
from git.exc import GitCommandError

# General gitlab CI variables
CI_PROJECT_ID = "CI_PROJECT_ID"
CI_API_V4_URL = "CI_API_V4_URL"
CI_COMMIT_BRANCH = "CI_COMMIT_BRANCH"
CI_PROJECT_PATH = "CI_PROJECT_PATH"
CI_SERVER_HOST = "CI_SERVER_HOST"
CI_SERVER_PORT = "CI_SERVER_PORT"


def ci_project_id() -> str:
    return os.getenv(CI_PROJECT_ID)


def ci_api_v4_url() -> str:
    return os.getenv(CI_API_V4_URL)


def ci_commit_branch() -> str:
    return os.getenv(CI_COMMIT_BRANCH)


def ci_project_path() -> str:
    return os.getenv(CI_PROJECT_PATH)


def ci_server_host() -> str:
    return os.getenv(CI_SERVER_HOST)


def ci_server_port() -> str:
    return os.getenv(CI_SERVER_PORT)


# Internal MDC specific environment variables
GIT_LOG = "GIT_LOG"
LATEST_TAG = "LATEST_TAG"
NEXT_TAG = "NEXT_TAG"
BUMP = "BUMP"
UPLOADS = "UPLOADS"
REBASE_BRANCH = "REBASE_BRANCH"
CI_TOKEN = "CI_TOKEN"
CI_USER = "CI_USER"
CI_USER_EMAIL = "CI_USER_EMAIL"
CI_READONLY_TOKEN = "CI_READONLY_TOKEN"
CI_READONLY_USER = "CI_READONLY_USER"
NEXUS_USERNAME = "NEXUS_USERNAME"
NEXUS_PASSWORD = "NEXUS_PASSWORD"
NEXUS_HOST = "NEXUS_HOST"


def ci_token() -> str:
    token = os.getenv(CI_TOKEN)
    if not token:
        raise EnvironmentError(f"Missing environment variable {CI_TOKEN}")
    return token


def ci_user() -> str:
    user = os.getenv(CI_USER)
    if not user:
        user = f"project_{ci_project_id()}_bot"
    return user


def ci_user_email() -> str:
    email = os.getenv(CI_USER_EMAIL)
    if not email:
        email = f"project{ci_project_id()}_bot@example.com"
    return email


def ci_readonly_token() -> str:
    token = os.getenv(CI_READONLY_TOKEN)
    if not token:
        return ci_token()
    return token


def ci_readonly_user() -> str:
    user = os.getenv(CI_READONLY_USER)
    if not user:
        return ci_user()
    return user


def nexus_username() -> str:
    return os.getenv(NEXUS_USERNAME)


def nexus_password() -> str:
    return os.getenv(NEXUS_PASSWORD)


def nexus_host() -> str:
    host = os.getenv(NEXUS_HOST)
    if not host:
        host = "nexus.wopr.inf.mdc"
    return host


git = Git(".")


def increment(tag: str) -> str:
    major = r"breaking-change|major"
    minor = r"feature|minor"

    if tag:
        commit_prefixes = re.sub(fr"({major}|{minor}):.*", r"\1",
                                 git.log("--no-merges", '--pretty=format:%s', f"{tag}..HEAD"))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into '{ci_commit_branch()}'", r"\1",
                                 git.log("--merges", "--oneline", f"{tag}..HEAD"))
    else:
        commit_prefixes = re.sub(fr"({major}|{minor}):.*", r"\1", git.log("--no-merges", '--pretty=format:%s'))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into '{ci_commit_branch()}'", "\1",
                                 git.log("--merges", "--oneline"))

    if re.match(major, commit_prefixes) or re.match(major, branch_prefixes):
        return "major"
    if re.match(minor, commit_prefixes) or re.match(minor, branch_prefixes):
        return "minor"
    return "patch"


def create_release(tag: str, log: str):
    response = requests.post(f"{ci_api_v4_url()}/projects/{ci_project_id()}/releases",
                             json={"name": tag, "tag_name": tag, "description": f"""## Changelog\n\n{log}"""},
                             headers={"PRIVATE-TOKEN": ci_token(), "Content-Type": "application/json"})

    if response.status_code >= 400:
        raise HTTPError(response.status_code)


def env(args: list) -> dict:
    e = parse_common_flags(args)

    tag = latest_tag()
    e[LATEST_TAG] = tag

    bump_amount = increment(tag)
    e[BUMP] = bump_amount

    release_tag = next_tag(tag, bump_amount)
    e[NEXT_TAG] = release_tag

    log = git_log(tag)
    e[GIT_LOG] = log

    return e


def parse_common_flags(args: list) -> dict:
    env_dict = dict()
    parser = argparse.ArgumentParser()

    parser.add_argument('--rebase-branch', '-r')
    parser.add_argument('--uploads', '-u')

    args, _ = parser.parse_known_args(args)

    env_dict[REBASE_BRANCH] = args.rebase_branch or ""
    env_dict[UPLOADS] = args.uploads or ""

    return env_dict


def next_tag(tag: str, bump: str) -> str:
    if not tag:
        return "0.0.1"
    ver = semver.VersionInfo.parse(tag.lstrip("v"))
    return str(ver.next_version(bump))


def git_log(tag: str = None) -> str:
    if tag:
        log = git.log("--oneline", "--no-merges", f"{tag}..HEAD")
    else:
        log = git.log("--oneline", "--no-merges")
    return sanitize(repr(log).strip("'"))


def sanitize(log: str) -> str:
    sanitized_log = re.sub('&', '&amp;', log)
    sanitized_log = re.sub('<', '&lt;', sanitized_log)
    sanitized_log = re.sub('>', '&gt;', sanitized_log)
    sanitized_log = re.sub('"', '&quot;', sanitized_log)
    sanitized_log = re.sub("'", "&#39;", sanitized_log)
    sanitized_log = re.sub(r'\\n', r'<br/>', sanitized_log)
    return sanitized_log


def latest_tag() -> str:
    try:
        return git.describe("--abbrev=0")
    except GitCommandError:
        return ""


def rebase(branch=None):
    if not branch:
        branch = get_rebase_branch()

    if not branch:
        print("No rebase branch, skipping...", file=sys.stderr)
        return

    print(f"Checking out {branch}", file=sys.stderr)
    git.checkout(branch)

    print(f"Rebasing {branch} onto {ci_commit_branch()}", file=sys.stderr)
    git.rebase(ci_commit_branch())

    print(f"Pushing changes to {branch}", file=sys.stderr)
    git.push("origin", branch)


def get_rebase_branch() -> str:
    branches = ["develop", "dev"]
    for branch in branches:
        try:
            git.show_ref("--verify", "--quiet", f"refs/remotes/origin/{branch}")
            return branch
        except GitCommandError:
            pass
    return ""


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


def config_git():
    git.remote("set-url", "origin", f"https://{ci_user()}:{ci_token()}@{ci_server_host()}/{ci_project_path()}.git")
    git.config("user.name", ci_user())
    git.config("user.email", ci_user_email())
    git.fetch("--all", "--tags")
    git.checkout(ci_commit_branch())
    git.pull("origin", ci_commit_branch())


def create_attachment(pattern: str, tag: str):
    for file in glob.glob(pattern, recursive=True):
        with open(file, 'rb') as f:
            response = requests.post(f"{ci_api_v4_url()}/projects/{ci_project_id()}/uploads",
                                     files={'file': f},
                                     headers={"PRIVATE-TOKEN": ci_token()})

            if response.status_code >= 400:
                raise HTTPError(response.status_code)

        link = response.json()['full_path']
        response = requests.post(f"{ci_api_v4_url()}/projects/{ci_project_id()}/releases/{tag}/assets/links",
                                 data={"name": file, "url": link},
                                 headers={"PRIVATE-TOKEN": ci_token()})
        if response.status_code >= 400:
            raise HTTPError(response.status_code)


def version(tag: str):
    git.commit("--allow-empty", "-am", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")


def short_sha() -> str:
    return git.rev_parse("--short", "HEAD")
