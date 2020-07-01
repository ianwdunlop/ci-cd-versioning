#! /bin/bash
# Intended for use in an ubuntu image.

function previous_tag() {
  tag=$(git tag --sort=-committerdate | sed -n "s/^$1-\(v[0-9]\.[0-9]\.[0-9]\)$/\1/p")
  if [ -z "$tag" ]; then
    tag="none"
  fi
  echo "$tag"
}

if [ $# -lt 1 ]; then
  echo "usage: ./release.sh [common|python|scala|node|golang]"
fi

# Install dependencies
apt-get update -yqq && apt-get install -yqq apt-transport-https ca-certificates curl gnupg git bc

. ./common/utils.sh

# Set up git
. ./common/setup-git.sh

# Parse flags
. ./common/parse-common-flags.sh

IMAGE=$(trim "$PARAMS")

# Previous tag for the inputted language
PREVIOUS_TAG=$(previous_tag "$IMAGE")

# Previous tag gives log of work done since last merge to master.
PREVIOUS_TAG_GENERAL=$(./common/previous-tag.sh)
reportError $?

GIT_LOG=$(./common/git-log.sh "$PREVIOUS_TAG_GENERAL")
reportError $?
export GIT_LOG

BUMP=$(./common/bump.sh "$PREVIOUS_TAG_GENERAL")
reportError $?

RELEASE_TAG="$IMAGE-$(./common/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
reportError $?

git commit --allow-empty -am "Setting version to $RELEASE_TAG"
git tag -a "$RELEASE_TAG" -m "Setting version to $RELEASE_TAG"
git push origin "$CI_COMMIT_BRANCH"
git push origin --tags
. ./common/create-release.sh

if [[ $IMAGE == "common" ]]; then
  PREVIOUS_TAG=$(previous_tag python)
  reportError $?
  RELEASE_TAG="python-$(./common/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
  reportError $?
  git commit --allow-empty -am "Setting version to $RELEASE_TAG"
  git tag -a "$RELEASE_TAG" -m "Setting version to $RELEASE_TAG"
  git push origin "$CI_COMMIT_BRANCH"
  git push origin --tags
  . ./common-release.sh

  PREVIOUS_TAG=$(previous_tag node)
  reportError $?
  RELEASE_TAG="node-$(./common/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
  reportError $?
  git commit --allow-empty -am "Setting version to $RELEASE_TAG"
  git tag -a "$RELEASE_TAG" -m "Setting version to $RELEASE_TAG"
  git push origin "$CI_COMMIT_BRANCH"
  git push origin --tags
  . ./common-release.sh

  PREVIOUS_TAG=$(previous_tag scala)
  reportError $?
  RELEASE_TAG="scala-$(./common/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
  reportError $?
  git commit --allow-empty -am "Setting version to $RELEASE_TAG"
  git tag -a "$RELEASE_TAG" -m "Setting version to $RELEASE_TAG"
  git push origin "$CI_COMMIT_BRANCH"
  git push origin --tags
  . ./common-release.sh

  PREVIOUS_TAG=$(previous_tag scala)
  reportError $?
  RELEASE_TAG="scala-$(./common/next-tag.sh "$PREVIOUS_TAG" "$BUMP")"
  reportError $?
  git commit --allow-empty -am "Setting version to $RELEASE_TAG"
  git tag -a "$RELEASE_TAG" -m "Setting version to $RELEASE_TAG"
  git push origin "$CI_COMMIT_BRANCH"
  git push origin --tags
  . ./common-release.sh

fi
