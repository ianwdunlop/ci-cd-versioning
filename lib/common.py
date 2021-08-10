from git.cmd import Git
from git.exc import GitCommandError
import re
import os
import sys
import argparse
import semver
import requests
from requests.models import HTTPError
import glob

# General gitlab CI variables
CI_PROJECT_ID = "CI_PROJECT_ID"
CI_API_V4_URL = "CI_API_V4_URL"
CI_COMMIT_BRANCH = "CI_COMMIT_BRANCH"
CI_PROJECT_PATH = "CI_PROJECT_PATH"
CI_SERVER_HOST = "CI_SERVER_HOST"
CI_SERVER_PORT = "CI_SERVER_PORT"

ci_project_id = os.getenv(CI_PROJECT_ID)
ci_api_v4_url = os.getenv(CI_API_V4_URL)
ci_commit_branch = os.getenv(CI_COMMIT_BRANCH)
ci_project_path = os.getenv(CI_PROJECT_PATH)
ci_server_host = os.getenv(CI_SERVER_HOST)
ci_server_port = os.getenv(CI_SERVER_PORT)

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
NEXUS_USERNAME = "NEXUS_USERNAME"
NEXUS_PASSWORD = "NEXUS_PASSWORD"
NEXUS_HOST = "NEXUS_HOST"


def get_ci_token() -> str:
    ci_token = os.getenv(CI_TOKEN)
    if not ci_token:
        raise EnvironmentError(f"Missing environment variable {CI_TOKEN}")
    return ci_token


ci_user = os.getenv(CI_USER)
if not ci_user:
    ci_user = f"project_{ci_project_id}_bot"

ci_user_email = os.getenv(CI_USER_EMAIL)
if not ci_user_email:
    ci_user_email = f"project{ci_project_id}_bot@example.com"

nexus_username = os.getenv(NEXUS_USERNAME)
nexus_password = os.getenv(NEXUS_PASSWORD)
nexus_host = os.getenv(NEXUS_HOST)
if not nexus_host:
    nexus_host = "nexus.wopr.inf.mdc"

git = Git(".")


def increment(tag: str) -> str:
    major = r"breaking-change|major"
    minor = r"feature|minor"

    if tag:
        commit_prefixes = re.sub(fr"({major}|{minor}):.*", r"\1",
                                 git.log("--no-merges", '--pretty=format:%s', f"{tag}..HEAD"))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into '{ci_commit_branch}'", r"\1",
                                 git.log("--merges", "--oneline", f"{tag}..HEAD"))
    else:
        commit_prefixes = re.sub(fr"({major}|{minor}):.*", r"\1", git.log("--no-merges", '--pretty=format:%s'))
        branch_prefixes = re.sub(fr".*Merge branch '({major}|{minor})/.*' into '{ci_commit_branch}'", "\1",
                                 git.log("--merges", "--oneline"))

    if re.match(major, commit_prefixes) or re.match(major, branch_prefixes):
        return "major"
    elif re.match(minor, commit_prefixes) or re.match(minor, branch_prefixes):
        return "minor"
    else:
        return "patch"


def create_release(tag: str, log: str):
    response = requests.post(f"{ci_api_v4_url}/projects/{ci_project_id}/releases",
                             json={"name": tag, "tag_name": tag, "description": f"##Changelog\n\n{log}"},
                             headers={"PRIVATE-TOKEN": get_ci_token()})

    if response.status_code >= 400:
        raise HTTPError


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

    if args.rebase_branch:
        env_dict[REBASE_BRANCH] = args.rebase_branch

    if args.uploads:
        env_dict[UPLOADS] = args.uploads

    return env_dict


def next_tag(tag: str, bump: str) -> str:
    if not tag:
        return "0.0.1"
    ver = semver.VersionInfo.parse(tag.lstrip("v"))
    return str(ver.next_version(bump))


def git_log(tag: str) -> str:
    log = git.log("--oneline", "--no-merges", f"{tag}..HEAD")
    return sanitize(repr(log).strip("'"))


def sanitize(log: str) -> str:
    sanitized_log = re.sub('&', '&amp;', log)
    sanitized_log = re.sub('<', '&lt;', sanitized_log)
    sanitized_log = re.sub('>', '&gt;', sanitized_log)
    sanitized_log = re.sub('"', '&quot;', sanitized_log)
    sanitized_log = re.sub("'", "&#39;", sanitized_log)
    return sanitized_log


def latest_tag() -> str:
    try:
        return git.describe("--abbrev=0")
    except GitCommandError:
        return ""


def rebase():
    branch = get_rebase_branch()
    if not branch:
        print("No rebase branch, skipping...", file=sys.stderr)
        return

    print(f"Checking out {branch}", file=sys.stderr)
    git.checkout(branch)

    print(f"Rebasing {branch} onto {ci_commit_branch}", file=sys.stderr)
    git.rebase(ci_commit_branch)

    print(f"Pushing changes to {branch}", file=sys.stderr)
    git.push("origin", branch)


def get_rebase_branch() -> str:
    branch = os.getenv(REBASE_BRANCH)
    if branch:
        return branch

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
    version(tag)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase()


def config_git():
    git.remote("set-url", "origin", f"https://{ci_user}:{get_ci_token()}@{ci_server_host}/{ci_project_path}.git")
    git.config("user.name", ci_user)
    git.config("user.email", ci_user_email)
    git.fetch("--all", "--tags")
    git.checkout(ci_commit_branch)
    git.pull("origin", ci_commit_branch)


def create_attachment(pattern: str, tag: str):
    for file in glob.glob(pattern, recursive=True):
        f = open(file, 'rb')
        response = requests.post(f"{ci_api_v4_url}/projects/{ci_project_id}/uploads",
                                 files={'file': f},
                                 headers={"PRIVATE-TOKEN": get_ci_token()})
        f.close()
        if response.status_code >= 400:
            raise HTTPError

        link = response.json()['full_path']
        response = requests.post(f"{ci_api_v4_url}/projects/{ci_project_id}/releases/{tag}/assets/links",
                                 data={"name": file, "url": link},
                                 headers={"PRIVATE-TOKEN": get_ci_token()})
        if response.status_code >= 400:
            raise HTTPError


def version(tag: str):
    git.commit("--allow-empty", "-am", f'"Setting version to {tag}"')
    git.push("origin", ci_commit_branch)
    git.tag("-a", tag, "-m", f"Setting version to {tag}")
    git.push("origin", "--tags")


def short_sha() -> str:
    return git.rev_parse("--short", "HEAD")
