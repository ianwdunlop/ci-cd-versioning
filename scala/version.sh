#! /bin/bash

sbt "release with-defaults release-version $RELEASE_VERSION next-version $NEXT_VERSION"