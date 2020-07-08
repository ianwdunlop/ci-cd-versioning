#!/bin/bash

if git describe --abbrev=0 &> /dev/null; then
  git describe --abbrev=0
else
  echo "none"
fi




