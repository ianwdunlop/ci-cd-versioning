# Continuous Integration

> Shared repository for base images to use in CI/CD.

All images:
* Are based on [debian](https://www.debian.org/).
* Contain useful scripts in the `/scripts` folder and available on the `PATH`.
* Are simple to use out of the box. Most CI will need only `release.sh`.

## Usage
Example `.gitlab-ci.yml` files are available for each supported language:
* [Python](python/gitlab-ci.example.yml).
* [Node](node/gitlab-ci.example.yml).
* [Scala](scala/gitlab-ci.example.yml).
* [Golang](golang/gitlab-ci.example.yml).

If using these images for your CI, it is recommended that you **always** create merge 
commits, and **never** squash your commits. These are the default options in gitlab.

## Images
Overview of the images, their use cases, and the usage of the scripts they contain.

### Common
Available at `registry.mdcatapult.io/informatics/docker-images/ci` and based on
`debian:buster`, this image contains base scripts which are useful for the release
process of all languages. It is preinstalled with some apt packages to meet the 
dependencies of the scripts. The following scripts are included:

#### `parse-common-flags.sh`
Parses flags that are common to all `release.sh` scripts and exports appropriate 
environment variables. The supported flags are:
* `-r --rebase [branch]` specify a branch to rebase onto (optional, rebase will still point to `develop` or `dev` if missing).
This sets the `REBASE_BRANCH` environment variable.
* `-u --uploads` file glob for files to add to the release. The files **MUST** be 
present before running any `release.sh` scripts. This sets the `UPLOADS` environment
variable.

Any remaining arguments are concatenated in a space separated list and exported as 
`PARAMS`. 

#### `setup-git.sh`
Sets up the CI git user to track the `CI_COMMIT_BRANCH`. Requires the following 
environment variables to be set:
* `CI_USER`: CI username configured in gitlab.
* `CI_USER_EMAIL`: CI user email configured in gitlab.
* `CI_USER_TOKEN`: CI user api token with read/write access.

#### `previous-tag.sh`
Returns the previous tag if there is one. Returns `none` otherwise.

#### `bump.sh`
Interprets the git log between HEAD and the given tag to determine which version 
to bump. Requires a tag to be passed as a **command line argument**. Returns `major`, `minor`, or 
`patch`.

For the commit message prefix strategy, the prefixes `feature:` and `breaking-change:`
if found will increment the minor or major version respectively. A major version 
increment will take precedent of a minor increment.

For the branch prefix strategy, the prefixed `feature/` and `breaking-change/` are 
handled in the same way.

#### `next-tag.sh`
Takes a [semver comformant](https://semver.org/) tag and the version to bump (`major|minor|patch`) 
as command line arguments. Returns a version with the bump applied. e.g.:
```bash
/scripts/next-version.sh v1.0.1 minor
v1.1.0
```
The optional flag `--no-prefix` gives the same version without a `v`.

#### `git-log.sh`
Returns a prettyfied git log between HEAD and the given tag (or `none` if there is no 
tag) for use as a changelog.

#### `utils.sh`
Contains utility functions `reportError` for checking the error code of a child script
and `trim` for trimming whitespace from a bash variable.

#### `rebase.sh`
Attempts to rebase `REBASE_BRANCH` onto `CI_COMMIT_BRANCH` if it has been set. 
Otherwise, the script will look for branches called `develop` or `dev` and rebases those instead. 
If the rebase fails, this script should error.

#### `create-release.sh`
Uses `curl` to create a formatted release in the gitlab project. Requires the 
following environment variables to be set:
* `CI_TOKEN`: gitlab API token configured as a CI variable in gitlab.
* `RELEASE_TAG`: the tag being released against. There must be a matching tag in the
repository.
* `GIT_LOG`: This can be outputted by `git-log.sh`.

If `UPLOADS` has been set via the flag parser, `create-release.sh` will then call `upload-files.sh`
with `UPLOADS` and `RELEASE_TAG`.

#### `upload-files.sh`
Uploads files to the specified release. Takes a file glob and the release tag as command 
line arguments. e.g.
```bash
/scripts/upload-files.sh builds/* v1.0.1
```
This script expects the following environment variables to be set:
* `CI_TOKEN`: API token configured as a CI variable in gitlab.

#### `version.sh`
Does the following:
1. Adds an empty commit with the message to "Setting version to..." for CI purposes.
2. Pushes the commit.
3. Tags the commit with `RELEASE_TAG` and pushes the tag.

#### `release.sh`
Does the following:
1. Sources `utils.sh` to make utility functions available.
2. Sources `setup-git.sh` to set up git.
3. Sources `export-env.sh` with `$@` to pass down it's command line arguments.
4. Sources `version.sh` to run the versioning procedure (and export `RELEASE_TAG`)
5. Sources `create-release.sh` to push the release to gitlab.
6. Calls `rebase.sh` to rebase if required.

### Python
Available at `registry.mdcatapult.io/informatics/docker-images/ci/python` and based on `python:latest`. A Python 3.6 version is available at `registry.mdcatapult.io/informatics/docker-images/ci/python:3.6`.
Scripts in `python` and `common` are copied to `/scripts`.
Scripts with the same filename are overwritten by the files in `python`.
The default pip cache is `/root/.cache/pip`. This can be overridden by setting the `PIP_CACHE_DIR` environment variable.

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `VERSION_DIR`: The directory containing the `version.py` file.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `RELEASE_TAG`: The tag to release with.
* `RELEASE_VERSION`: The same as the release tag but without a prefix.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.
* `NEXT_VERSION`: The alpha pre-release version of the next anticipated release. This 
is a patch on the release version suffixed with "a0" (i.e. if the release version is 
1.0.1, the next version is 1.0.2a0). The next version isn't guaranteed to be honoured.

#### `write-version.sh`
Takes the version to be written as a command line argument. Requires that the 
`VERSION_DIR` environment variable is set. If a `version.py` exists in `VERSION_DIR` 
the lines containing `__version__` and `__hash__` are cut, and the new version and 
hash (commit short sha of HEAD) are appended. Otherwise, a new file is written with
the same information.

#### `version.sh`
Does the following:
1. Calls `write-version.sh` to write the new version.
2. Commits and pushes those changes on `CI_COMMIT_BRANCH`.
3. Tags the commit with the release tag and pushes the tag to gitlab.
4. Calls `write-version.sh` to write the next version.
5. Commits and pushes the changes on `CI_COMMIT_BRANCH`.

#### `release.sh`
Requires that the folder containing `version.py` is passed in as a command line 
argument.
Does the following:
1. Sources `utils.sh` to make utility functions available.
2. Sources `setup-git.sh` to set up git.
3. Sources `export-env.sh` with `$@` to pass down it's command line arguments.
4. Sources `version.sh` to run the versioning procedure.
5. Sources `create-release.sh` to push the release to gitlab.
6. Calls `rebase.sh` to rebase if required.

### Node
Available at `registry.mdcatapult.io/informatics/docker-images/ci/node` and based on `node:buster`.
Scripts in `node` and `common` are copied to `/scripts`.
Scripts with the same filename are overwritten by the files in `node`.

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.

#### `version.sh`
Does the following:
1. Calls npm version with `BUMP` and exports the result at `RELEASE_TAG`.
2. Pushes the changes and tag to git.

### Scala
Available at `registry.mdcatapult.io/informatics/docker-images/ci/scala` and based on `openjdk:buster`.
Scripts in `scala` and `common` are copied to `/scripts`.
Scripts with the same filename are overwritten by the files in `scala`.
Sbt will cache all scala and java packages under a directory
called `sbt-cache`, which is local to wherever `sbt` was called from.

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `RELEASE_TAG`: The tag to release with.
* `RELEASE_VERSION`: The release version to supply `sbt release` with.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.
* `NEXT_VERSION`: The next version to supply `sbt release` with. This is the SNAPSHOT
version of the next anticipated release, which is always a patch on the release version
(as with the python releases).

#### `version.sh`
Does the following:
1. Calls `sbt "release with-defaults"` with the `RELEASE_VERSION` and `NEXT_VERSION`.

### Golang
Available at `registry.mdcatapult.io/informatics/docker-images/ci/golang` and based on `golang:latest`. 
Scripts in `golang` and `common` are copied to `/scripts`.
Scripts with the same filename are overwritten by the files in `golang`.

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `RELEASE_TAG`: The tag to release with.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.

#### `setup-go-private.sh`
Writes a `~/.netrc` file using the `gitlab-ci-token` user and the `$CI_JOB_TOKEN` password. This makes the CI image capable of go getting private modules from gitlab. Note that the permissions of the job token are the same as the user that triggered the job.
