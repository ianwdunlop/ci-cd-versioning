# Continuous Integration

> Shared repository for base images to use in CI/CD.

Each language specific image uses the `common` image as a base. All scripts in `common` are moved into the `/scripts` folder. It is important that script 
names in a language specific folder do not collide with those in `common`.

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
Available at `registry.mdcatapult.io/informatics/docker-images/ci:common` and based on
`ubuntu:20.04`, this image contains base scripts which are useful for the release
process of all languages. It is preinstalled with some apt packages to meet the 
dependencies of the scripts. The following scripts are included:

#### `parse-common-flags.sh`
Parses flags that are common to all `release.sh` scripts and exports appropriate 
environment variables. The supported flags are:
* `-r --rebase [branch]` specify a branch to rebase onto (optional, default none).
This sets the `REBASE_BRANCH` environment variable.
* `-c --commits` use commit message prefixes to determine which version tier to bump 
(this is the default). This sets the `VERSIONING_STRATEGY` environment variable.
* `-b --branches` use branch prefixes to determine which version to bump. This sets 
the `VERSIONING_STRATEGY` environment variable.

Any remaining arguments are concatenated in a space separated list and exported as 
`PARAMS`. 

#### `setup-git.sh`
Sets up the CI git user to track the `CI_COMMIT_BRANCH`. Requires the following 
environment variables to be set:
* `SSH_PRIVATE_KEY`: ssh key configured in gitlab.
* `CI_PROJECT_PATH`: set automatically by gitlab.
* `GIT_RELEASE_USER`: CI username configured in gitlab.
* `GIT_RELEASE_EMAIL`: CI user email configured in gitlab (must match email in 
`SSH_PRIVATE_KEY`).
* `CI_COMMIT_BRANCH`:  set automatically by gitlab (represents the branch that the 
pipeline is running against).

#### `previous-tag.sh`
Returns the previous tag if there is one. Returns `none` otherwise.

#### `bump.sh`
Interprets the git log between HEAD and the given tag to determine which version 
to bump. Requires a tag to be passed as a **command line argument**. Requires the 
`VERSIONING_STRATEGY` environment variable to be set to `commits` (default) or 
`branches` (see [parsing](#parse-common-flags.sh)). Returns `major`, `minor`, or 
`patch`.

For the commit message prefix strategy, the prefixes `feature:` and `breaking-change:`
if found will increment the minor or major version respectively. A major version 
increment will take precedent of a minor increment.

For the branch prefix strategy, the prefixed `feature/` and `breaking-change/` are 
handled in the same way.

#### `next-tag.sh`
Takes a semver comformant tag and the version to bump (`major|minor|patch`) 
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
Attempts to rebase `REBASE_BRANCH` onto `CI_COMMIT_BRANCH`. If `REBASE_BRANCH` 
is empty no rebase is attempted. If the rebase fails, this script will print a 
warning but will exit with `0`.

#### `create-release.sh`
Uses `curl` to create a formatted release in the gitlab project. Requires the 
following environment variables to be set:
* `GIT_RELEASE_TOKEN`: gitlab API token configured as a CI variable in gitlab.
* `RELEASE_TAG`: the tag being released against. There must be a matching tag in the
repository.
* `GIT_LOG`: This can be outputted by `git-log.sh`.
* `CI_PROJECT_ID`: set automatically by gitlab.

### Python
Available at `registry.mdcatapult.io/informatics/docker-images/ci:python` and based 
on `registry.mdcatapult.io/informatics/docker-images/ci:common`. It is preinstalled with 
all python dependencies (i.e. libsqlite3-dev), Python3.7.7, pip, and twine. Scripts in 
`python` are moved into `scripts` (in which the scripts from `common` are also located).

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `VERSIONING_STRATEGY`: The strategy to use when determining the version to 
increment.
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
5. Sources `rebase.sh` to rebase if required.
6. Sources `create-release.sh` to push the release to gitlab.

### Node
Available at `registry.mdcatapult.io/informatics/docker-images/ci:node` and based 
on `registry.mdcatapult.io/informatics/docker-images/ci:common`. It is preinstalled with 
node v12.16.2 LTS and google chrome (for running tests in a headless browser). Scripts 
in `node` are moved into `scripts` (in which the scripts from `common` are also located).

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `VERSIONING_STRATEGY`: The strategy to use when determining the version to 
increment.
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.

#### `version.sh`
Does the following:
1. Calls npm version with `BUMP` and exports the result at `RELEASE_TAG`.
2. Pushes the changes and tag to git.

#### `release.sh`
Does the following:
1. Sources `utils.sh` to make utility functions available.
2. Sources `setup-git.sh` to set up git.
3. Sources `export-env.sh` with `$@` to pass down it's command line arguments.
4. Sources `version.sh` to run the versioning procedure (and export `RELEASE_TAG`)
5. Sources `rebase.sh` to rebase if required.
6. Sources `create-release.sh` to push the release to gitlab.

### Scala
Available at `registry.mdcatapult.io/informatics/docker-images/ci:scala` and based 
on `registry.mdcatapult.io/informatics/docker-images/ci:common`. It is preinstalled with 
Openjdk 14 and sbt. Scripts in `scala` are moved into `scripts` (in which the scripts 
from `common` are also located).

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `VERSIONING_STRATEGY`: The strategy to use when determining the version to 
increment.
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

#### `release.sh`
Does the following:
1. Sources `utils.sh` to make utility functions available.
2. Sources `setup-git.sh` to set up git.
3. Sources `export-env.sh` with `$@` to pass down it's command line arguments.
4. Sources `version.sh` to run the versioning procedure.
5. Sources `rebase.sh` to rebase if required.
6. Sources `create-release.sh` to push the release to gitlab.

### Golang
Available at `registry.mdcatapult.io/informatics/docker-images/ci:golang` and based 
on `registry.mdcatapult.io/informatics/docker-images/ci:common`. It is preinstalled with 
go version 1.14.4 and sets up the go environment in the standard way. Scripts in `golang`
are moved into `scripts` (in which the scripts from `common` are also located).

#### `export-env.sh`
Interprets the command line arguments and git history using scripts from `common` to 
export the following environment variables:
* `VERSIONING_STRATEGY`: The strategy to use when determining the version to 
increment.
* `REBASE_BRANCH`: The branch to rebase, if any.
* `PARAMS`: Remaining command line arguments not consumed by `parse-common-flags.sh`.
* `PREVIOUS_TAG`: The previous git tag.
* `BUMP`: The version to bump.
* `RELEASE_TAG`: The tag to release with.
* `GIT_LOG`: Prettyfied git log for use in gitlab release.

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
4. Sources `version.sh` to run the versioning procedure.
5. Sources `rebase.sh` to rebase if required.
6. Sources `create-release.sh` to push the release to gitlab.