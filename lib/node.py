from subprocess import check_call
from lib.common import (
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    REBASE_BRANCH,
    ci_commit_branch,
    create_release,
    env,
    rebase,
    set_git_config,
    fetch_all_and_checkout_latest,
    create_attachment,
    git
)


def release(args: list):
    set_git_config()
    fetch_all_and_checkout_latest()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]

    for arg in args: 
        if '--release-path-1' in arg:
            create_multiple_releases(args, tag, log)
            return 
    
    version(tag)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)

# Creates multiple releases based on --release-tag-X and --release-path-X args.
# A release's tag will be the base tag plus --release-tag-X, separated by '-'. Trailing '-' chars are removed.
def create_multiple_releases(args: list, tag, log):
    for arg in args:
        if '--release-tag-1' in arg:
            release_tag_1 = tag + '-' + arg.split('=')[1]
            release_tag_1 = release_tag_1.strip('-')
        if '--release-path-1' in arg:
            release_path_1 = arg.split('=')[1]
        if '--release-tag-2' in arg:
            release_tag_2 = tag + '-' + arg.split('=')[1]
            release_tag_2 = release_tag_2.strip('-')
        if '--release-path-2' in arg:
            release_path_2 = arg.split('=')[1]

    for release_params in [[release_tag_1, release_path_1], [release_tag_2, release_path_2]]:

        [release_tag, release_path] = release_params

        version(release_tag)
        create_release(release_tag, log)
        create_attachment(release_path, release_tag)


def version(tag: str):
    # Call with --no-git-tag-version then commit and tag manually
    # afterwards. Otherwise this will fail if the npm project is
    # located in a subfolder.
    check_call(["npm", "--no-git-tag-version", "version", tag])
    
    git.commit("-am", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
