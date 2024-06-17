# Continuous Integration & Code Versioning for Gitlab CI/CD pipelines

> Shared repository for base images to use in gitlab CI/CD pipelines.

## What does it do?

**tl/dr** Updates the semantic version of your code when you release it. Bumps versions for the languages `golang`, `Node`, `R`, `Python` & `SBT` ie `Scala`.

## How does it do it?

On a merge to the default branch (nowadays in gitlab this is called `main`) it updates the semantic version of the code, creates a tag based on that version and then creates
the next snapshot version and rebases back on to develop in readiness for the next release.  
Note: It doesn't have to be `main` but can be whatever branch you want as long as you have configured your default branch correctly.

## How do I use it via a CI file?

All the language subfolders contain an example of a gitlab CI file. Use one of the language based images in your ci process and then
to update the version/release the code use the cictl command to release it. For example, for python you could use the image `registry.gitlab.com/medicines-discovery-catapult/informatics/docker-images/ci/python:3.12` and release/version with `cictl exec release python src`.

## How do I get a patch/minor/major semantic version change
Prefix the branch name following these rules:
* For major version bump eg 2.1.3 to 3.0.0 prefix the branch name with `breaking-change` or `major`
`breaking-change/whatever-you-want`
`major/whatever-you-want`
* For minor version bump eg 2.1.3 to 2.2.0 prefix the branch name with `feature` or `minor`
`feature/whatever-you-want`
`minor/whatever-you-want`
* For patch version bump it is the default behaviour eg 2.1.3 to 2.1.4
`call-the-branch anything`

## Gotchas
* If using these images for your CI process, it is recommended that you **always** create merge commits, and **never** squash your commits. These are the default options in gitlab.
* Ensure that the push rules in your `Repository>Push rules` settings allow unverified users to push code. This is so that the bot user can tag & rebase the branch.
* Make sure you have created an access token called `CI_TOKEN` which is given `maintainer` access and read/write permissions.
* Ensure your project is allowed access to the CI images repo and, if you are using or pushing any packages, to the private gitlab package registry. Look at the `CI/CD>Token Access` settings.
* If you are running gitlab sast pipelines and using a private pypi repo then make sure to tell the CI stage using the `PIP_INDEX_URL` variable eg
```yaml
dependency_scanning:
  stage: test
  allow_failure: false
  inherit:
    default: false
  variables:
    SECURE_LOG_LEVEL: "debug"
    PIP_INDEX_URL: https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.com/api/v4/projects/${REGISTRY_HOST_PROJECT_ID}/packages/pypi/simple
```
* If you want to access any of the cictl commands beyond `release` then you may need to ensure that the correct env vars are available by running this command for the language in question: `source <(cictl config env golang)`.

### General project structure
All images:
* Are based on [debian](https://www.debian.org/).
* Contain the `cictl` command line interface tool. This is in the `/scripts` folder and on the path.
* Contain useful scripts in the `/scripts` folder and available on the `PATH`.
* Have an example `.gitlab-ci.yml` file within their folder.
* May come pre-installed with useful things. For example, the R image is based on the [R runner](https://gitlab.mdcatapult.io/informatics/docker-images/runners/-/tree/master/r) which has BioConductor and other packages pre-installed.
* To test the CI process you can see the instructions below but there is also a [CI Test repo](https://gitlab.mdcatapult.io/informatics/software-engineering/ci-test) which has a specific branch for each language to try out the branch to develop to master merge process.

Each language has a folder with a Dockerfile to create the image, a sample CI file and a `release.sh` file for legacy purposes.
Originally the CI processes were  written in bash scripts but they are now python based. Language specific commands are
in the `lib` folder.

```
├── cictl          # Main file to run CI commands. Figures out the command, language and calls the appropriate method
├── debian
│   ├── Dockerfile
│   └── release.sh
├── example.env    # Copy to .env, environment variables used by docker when running a CI container
├── golang
│   ├── Dockerfile
│   ├── gitlab-ci.example.yml
│   ├── godoc.sh # Utility script to generate godocs
│   └── release.sh
├── lib            # Language specific CI commands. Tell cictl which language to use eg cictl exec release node 
│   ├── common.py # Common CI commands shared between the language specific libs
│   ├── golang.py
│   ├── node.py
│   ├── python.py
│   └── sbt.py
├── node
│   ├── Dockerfile
│   ├── gitlab-ci.example.yml
│   └── release.sh
├── python
│   ├── Dockerfile
│   ├── gitlab-ci.example.yml
│   └── release.sh
├── sbt
│   ├── Dockerfile
│   ├── gitlab-ci.example.yml
│   └── release.sh
├── r
│   ├── Dockerfile
│   ├── gitlab-ci.example.yml
│   └── release.sh
```

## Usage
There are lots of commands, most of them are used internally by the release process, but you have access to them all if you need them.  

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
* `pip` configures pip to use an internal nexus host. - **DEPRECATED**

`cictl exec` executes the following:
* `rebase`: performs a rebase of `$REBASE_BRANCH`, `develop`, or `dev` (in order of precedence) onto the `$CI_COMMIT_BRANCH`. Typically, this is performed during a release when the `$CI_COMMIT_BRANCH` is master (i.e. we've just merged develop into master, so the pipeline is running on master), so develop is rebased onto master.
* `version`: performs various language dependent actions to increment the software version. If no language is specified, an empty commit is added and tagged with the given tag. Usage `cictl exec version tag <language(optional)>`.
* `release`: performs various language dependent actions to perform a full release. This includes configuring the environment, committing to the codebase, creating gitlab releases and attachments, and rebasing. Usage `cictl exec release <language(optional)>`.

Additionally, the golang image contains a script to obtain the raw html required to make godocs. This is located under `/scripts` as `godoc.sh`.

The variables used in the CI process in gitlab can be accessed via the gitlab Admin CI/CD pages. It is important that the
`CI_READONLY_USER` & `CI_READONLY_TOKEN` are for an actual current user and actually work! The default is the `project_bot`.

## Custom CI Environment Variables
You can override the following CI environment variables through gitlab settings for your repo.
`CI_DOMAIN`. The default is `noreply.gitlab.mdcatapult.io`.  
`CI_USER_EMAIL`. The default is project_`project_id`_bot@`CI_DOMAIN`. The `project_id` can be found on the home page of your repository underneath the title.  
eg project_702_bot@noreply.gitlab.mdcatapult.io. The CI pipeline will attempt to construct the correct email address for the `CI_TOKEN` that you created. If it gets it wrong you can set `CI_USER_EMAIL` with the correct one.  
This bot email/user is used to tag and rebase the release. If you look at the release pipeline you will see things like
```bash
INFO:git.cmd:git config user.name project_52267953_bot -> 0
INFO:git.cmd:git config user.email project_52267953_bot@noreply.gitlab.mdcatapult.io -> 0
```
`CI_READONLY_USER`. Used to generate the `netrc` file for go private repo
`CI_READONLY_TOKEN`. Used to generate the `netrc` file for go private repo

## cictl config pip deprecation
You can create a pip config file use `cictl config pip` which was mainly used when MDC had an internal `NEXUS` package repository. We now have use `gitlab` for the package registry
and recommend using the `index-url` and/or `extra-index-url` settings within the CI file itself like this:
```bash
test:
  stage: test
  script:
    - pip install -r requirements.txt --index-url https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.com/api/v4/projects/${REGISTRY_HOST_PROJECT_ID}/packages/pypi/simple
```
Note that here we use a CI variable called `REGISTRY_HOST_PROJECT_ID` to hide the actual project id. Don't forget to allow your project repo access to your package repository via the CI/CD settings.

*If you do* have an internal Nexus based package repo and want to create the pip config file then note the following (plus the fact that it will be removed in a future release):  
Set `PACKAGE_PASSWORD` to `true` if there is a password required to access the package repository and also set the `NEXUS_PASSWORD`, `NEXUS_USERNAME` and `NEXUS_HOST` variables. If you want to use `pypi` repo then do not set these variables.

## Adding and updating images

Some background on what happens in teh build process: Each language folder, `sbt`, `python` etc, has a Dockerfile that defines what goes into each image. The Dockerfile defines a `TAG` variable to determine what version of the upstream image
should be used. For example,
```bash
ARG TAG=latest
FROM python:$TAG
```
Within the projects `.gitlab-ci.yml` file there are various stages, eg `python3.11` that define the actual tagged image to be built. In this example it builds a `python:3.11` image:
```yaml
python3.11:
  stage: build
  script:
    - |
      /kaniko/executor --context $CI_PROJECT_DIR --dockerfile python/Dockerfile \
      --build-arg TAG=3.11 \
      --destination $CI_REGISTRY_IMAGE/python:3.11 \
      --destination $CI_REGISTRY_IMAGE/python:3.11-$CI_COMMIT_REF_NAME
```

Within each Dockerfile it also copies the `cictl` script and the `lib` folder. It also copies the internal MDC ssl certificates (note: it's not clear if these certificates are needed since the images are not used to run any services on the MDC kube cluster).

If you want to change an existing build then change the kaniko `--build-arg` that contains the `TAG` to something else. If you want to add a completely new image then copy an existing build stage
and change the kaniko command appropriately. There is usually an accompanying `-dev` stage for building images for branches.

## Development & Testing CI pipelines
Requires python3.6+, virtualenv and docker. The `example.env` file contains all the gitlab builtin environment variables that these scripts make use of. They have been set to values suitable for testing against the [CI Test repository](https://gitlab.mdcatapult.io/informatics/software-engineering/ci-test).
```bash
# environment:
git clone git@gitlab.com:medicines-discovery-catapult/informatics/docker-images/ci.git
cd ci
virtualenv -p python3.7 venv
source venv/bin/activate
pip install -r requirements.txt

# testing the commands directly:
# (fill out the .env file first)
cp example.env .env
set -a; source .env; set +a
source <(./cictl config env)
./cictl create release $NEXT_TAG 

# building & pushing test images:
docker build --pull -f debian/Dockerfile -t registry.gitlab.com/medicines-discovery-catapult/informatics/docker-images/ci/debian:test .
docker push registry.gitlab.com/medicines-discovery-catapult/informatics/docker-images/ci/debian:test

# testing images with a local repo:
# (fill out the .env file first)
cp example.env .env
docker build --pull -f debian/node -t ci-node-test .
docker run -it -v $LOCAL_REPO:/repo -w /repo --env-file .env ci-node-test
```

In the `docker build` phase there are 6 images possible:
* debian/Dockerfile
* node/Dockerfile
* golang/Dockerfile
* python/Dockerfile
* sbt/Dockerfile
* r/Dockerfile

**Make sure you choose the correct Dockerfile and tag before you push anything to the repo.**

### Running CI commands
From within a running CI container you can then test the `cictl` commands against the `LOCAL_REPO`. Remember that this will actually
run things against the repo in gitlab so be careful. For example here we are testing the `Aurac` release pipeline which will bump
versions, create a tag and release and attach the Aurac zip to it. Have a look an actual `.gitlab-ci.yml` file to see the 
commands that a CI pipeline is running. For example, in the Aurac release stage it executes:

```bash
/scripts/release.sh -b -r develop -u 'dist/browser-plugin/web-ext-artifacts/aurac-*.zip'
```

This `release.sh` script is in this repo in the `node` folder and just runs `cictl exec release node "$@"`. Look at the `cictl` code
in this repo's root folder to see what `exec` does. Basically it ends up calling the `release` method in the `lib/node.py` code. The same pattern
is followed for all languages. You don't have to use `/script/release.sh`, it is just there for legacy and you can call the commands
directly as shown below.

```bash
root@969f9dea6d82:/repo# cictl exec release node -b -r develop -u 'dist/browser-plugin/web-ext-artifacts/aurac-*.zip'
```

It might be easier to try the commands against a dummy repo that no-one cares about. There is also
the [CI test repo](https://gitlab.mdcatapult.io/informatics/software-engineering/ci-test) which is designed to work against a CI image in the registry. Clone the
project, create a branch eg `node-dev` that will be using your new pipeline. Change some code on it, change the .gitlab-ci.yml file
to use your CI image branch eg `node:test`, commit, push and watch the pipelines.

### Troubleshooting
If you have problems running the commands locally then pay close  attention to the logged output and double check your `.env` file. We have had issues where
the python interpreter treats quoted strings with env vars literally and we had to remove the quotes and
write them out long hand.

`"project_${CI_PROJECT_ID}_bot"` became `"project_550_bot"` etc.

Make sure that your `CI_PROJECT_ID`, `CI_TOKEN` & `CI_PROJECT_PATH` are correct and actually match the project that
you are testing.

**Remember this is all just code, none of it  is magic.**

## Some notes on R
If you look at the R example CI file you will see that it includes package upload to Nexus. Gitlab doesn't support R packages yet and we recommend using the [remotes package](https://remotes.r-lib.org/index.html).

### License
This project is licensed under the terms of the Apache 2 license, which can be found in the repository as `LICENSE.txt`
