#!/bin/bash

eval "$(ssh-agent -s)"
echo "${SSH_PRIVATE_KEY}" | ssh-add -

sbt "release with-defaults release-version $RELEASE_VERSION next-version $NEXT_VERSION"