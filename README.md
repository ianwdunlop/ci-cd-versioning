# Continuous Integration

> Shared repository for base images to use in gitlab CI/CD pipelines.

*If using these images for your CI, it is recommended that you **always** create merge commits, and **never** squash your commits. These are the default options in gitlab.*

All images:
* Are based on [debian](https://www.debian.org/).
* Contain the `cictl` command line interface tool. This is in the `/scripts` folder and on the path.
* Contain useful scripts in the `/scripts` folder and available on the `PATH`.
* Have an example `.gitlab-ci.yml` file within their folder.
* May come pre-installed with useful things. For example, the R image is based on the [R runner](https://gitlab.mdcatapult.io/informatics/docker-images/runners/-/tree/master/r) which has BioConductor and other packages pre-installed.
* To test the CI process you can see the instructions below but there is also a [CI Test repo](https://gitlab.mdcatapult.io/informatics/software-engineering/ci-test) which has a specific branch for each language to try out the branch to develop to master merge process.

### General structure
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
```

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

The variables used in the CI process in gitlab can be accessed via the [Admin Ci/CD pages](https://gitlab.mdcatapult.io/admin/application_settings/ci_cd). It is important that the
`CI_READONLY_USER` & `CI_READONLY_TOKEN` are for an actual current user and actually work!

## Custom CI Environment Variables
You can override the following CI environment variables through gitlab settings for your repo.
`CI_DOMAIN`. The default is `noreply.gitlab.mdcatapult.io`.  
`CI_USER_EMAIL`. The default is project_`project_id`_bot@`CI_DOMAIN`. The `project_id` can be found on the home page of your repository underneath the title.  
eg project_702_bot@noreply.gitlab.mdcatapult.io. The CI pipeline will attempt to construct the correct email address for the `CI_TOKEN` that you created. If it gets it wrong you can set `CI_USER_EMAIL` with the correct one.

Set `PACKAGE_PASSWORD` to `true` if there is a password required to access the package repository and also set the `NEXUS_PASSWORD`, `NEXUS_USERNAME` and `NEXUS_HOST` variables. If you want to use `pypi` repo then do not set these variables.
## Development & Testing CI pipelines
Requires python3.6+, virtualenv and docker. The `example.env` file contains all the gitlab builtin environment variables that these scripts make use of. They have been set to values suitable for testing against the [CI Test repository](https://gitlab.mdcatapult.io/informatics/software-engineering/ci-test).
```bash
# environment:
git clone git@gitlab.mdcatapult.io:informatics/docker-images/ci.git
cd ci
virtualenv -p python3.7 venv
source venv/bin/activate
echo -e "[global]\nindex = https://nexus.wopr.inf.mdc/repository/pypi-all/pypi\nindex-url = https://nexus.wopr.inf.mdc/repository/pypi-all/simple" > venv/pip.conf
pip install -r requirements.txt

# testing the commands directly:
# (fill out the .env file first)
cp example.env .env
set -a; source .env; set +a
source <(./cictl config env)
./cictl create release $NEXT_TAG 

# building & pushing test images:
docker build --pull -f debian/Dockerfile -t registry.mdcatapult.io/informatics/docker-images/ci/debian:test .
docker push registry.mdcatapult.io/informatics/docker-images/ci/debian:test

# testing images with a local repo:
# (fill out the .env file first)
cp example.env .env
docker build --pull -f debian/node -t ci-node-test .
docker run -it -v $LOCAL_REPO:/repo -w /repo --env-file .env ci-node-test
```

In the `docker build` phase there are 5 images possible:
* debian/Dockerfile
* node/Dockerfile
* golang/Dockerfile
* python/Dockerfile
* sbt/Dockerfile

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
