# Continuous Integration

Shared repository for scripts to execute within CI/CD tools.

## Creating release notes for scala projects

In the scala [gitlab CI file](scala/gitlab-ci.example.yml) the release notes are created using the following commands
```bash
export PREVIOUS_TAG=$(git describe --tags --abbrev=0)
export GIT_LOG=$(echo "$(git log $PREVIOUS_TAG..HEAD --oneline --no-merges)" | awk -v ORS='  \\n' '1')
export RELEASE_TAG=$(git describe --abbrev=0)
```
and added to the release using the gitlab API within the `description` parameter
```bash
 curl --header 'Content-Type: application/json'
      --header "PRIVATE-TOKEN: $GIT_RELEASE_TOKEN"
      --data "{ \"name\": \"$RELEASE_TAG\", \"tag_name\": \"$RELEASE_TAG\", \"description\": \"Changelog for $RELEASE_TAG\n\n$GIT_LOG\" }"
      --request POST https://gitlab.mdcatapult.io/api/v4/projects/$CI_PROJECT_ID/releases
```
