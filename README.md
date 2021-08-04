# Continuous Integration

> Shared repository for base images to use in CI/CD.

*If using these images for your CI, it is recommended that you **always** create merge commits, and **never** squash your commits. These are the default options in gitlab.*

All images:
* Are based on [debian](https://www.debian.org/).
* Contain the `cictl` command line interface tool. This is in the `/scripts` folder and on the path.
* Contain useful scripts in the `/scripts` folder and available on the `PATH`.

## Usage
`cictl` has the following commands:
* `get`: get a resource.
* `create`: create a resource.
* `config`: configure your environment.
* `exec`: execute an action.

`cictl get` can get the following resources:
* `latest-tag`: gets the last git tag.
* `git-log`: gets a formatted and sanitized git log which is safe for interacting with gitlab.
* `increment`: interprets the git log between head and a given tag and returns an appropriate version increment.
* `next-tag`: increments a given tag by a given amount.
* `short-sha`: gets the short-sha of the latest commit.

`cictl create` can create the following resources:
* `release`: creates a gitlab release against a given tag.
* `attachment`: creates attachments on a gitlab release, given a tag and a file glob.

`cictl config` can configure the following resources:
* `git`: configures git to use the ci user credentials (project token) and ensures we are up to date.
* `env`: returns a set of environment variables to export. It should be used like `source <(cictl config env <language(optional)>)`.
* `goprivate`: writes credentials to the `~/.netrc` file so that private go modules can be pulled. Must be used after `source <(cictl config env golang)`.
* `pip` configures pip to use our internal nexus host.

`cictl exec` executes the following:
* `rebase`: performs a rebase of `$REBASE_BRANCH`, `develop`, or `dev` (in order of precedence) onto the `$CI_COMMIT_BRANCH`. Typically, this is performed during a release when the `$CI_COMMIT_BRANCH` is master (i.e. we've just merged develop into master, so the pipeline is running on master), so develop is rebased onto master.
* `version`: performs various language dependent actions to increment the software version. If no language is specified, an empty commit is added and tagged with the given tag. Usage `cictl exec version tag <language(optional)>`.
* `release`: performs various language dependent actions to perform a full release. This includes configuring the environment, committing to the codebase, creating gitlab releases and attachments, and rebasing. Usage `cictl exec release <language(optional)>`.

Additionally, the golang image contains a script to obtain the raw html required to make godocs. This is located under `/scripts` as `godoc.sh`.

## Development
Requires python3.6+, virtualenv and docker.
```bash
# environment
git clone git@gitlab.mdcatapult.io:informatics/docker-images/ci.git
cd ci
virtualenv venv
. venv/bin/activate

# building & pushing test images
docker build --pull -f debian/Dockerfile -t registry.mdcatapult.io/informatics/docker-images/ci/debian:test .
docker push registry.mdcatapult.io/informatics/docker-images/ci/debian:test

# testing images with a local repo
# fill out the .env file first
cp example.env .env
docker run -it -v $LOCAL_REPO:/repo -w /repo --env-file .env test-image
```
