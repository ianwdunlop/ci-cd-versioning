from lib.common import (
    GIT_LOG,
    create_release,
    env,
    next_tag,
    rebase,
    config_git,
    NEXT_TAG,
    UPLOADS,
    short_sha,
    create_attachment,
    ci_commit_branch,
    nexus_username,
    nexus_password,
    nexus_host
)
from git.cmd import Git
from subprocess import call


def config_pip():
    index_path = "repository/pypi-all/pypi"
    index_url_path = "repository/pypi-all/simple"
    call(["pip", "config", "set", "global.index",
          f"https://{nexus_username}:{nexus_password}@{nexus_host}/{index_path}"])
    call(["pip", "config", "set", "global.index-url",
          f"https://{nexus_username}:{nexus_password}@{nexus_host}/{index_url_path}"])
    call(['pip', 'config', 'set', 'global.trusted-host', f'"{nexus_host}"'])


def release(version_dir: str):
    config_git()
    e = env()
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    next_version = next_tag(tag, "patch") + "a0"
    version(tag, next_version, version_dir)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase()


def version(tag: str, next_version: str, version_dir: str):
    git = Git(".")
    write_version(tag, _version_file(version_dir))
    git.add(_version_file(version_dir))
    git.commit("-m", f'"Setting version to {tag}"')
    git.push("origin", ci_commit_branch)
    git.tag("-a", tag, "-m", f"Setting version to {tag}")
    git.push("origin", "--tags")
    write_version(next_version, version_dir)
    git.commit("-am", f'"Setting version to {next_version}"')
    git.push("origin", ci_commit_branch)


def write_version(tag: str, version_dir: str):
    hash = short_sha()
    with open(_version_file(version_dir), "w") as f:
        f.writelines([f"__version__ = \"{tag}\"\n", f"__hash__ = \"{hash}\"\n"])


def _version_file(dir: str) -> str:
    return f"{dir}/version.py"
