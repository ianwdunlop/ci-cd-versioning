#! /bin/bash

pip config set global.trusted-host nexus.mdcatapult.io
pip config set global.index "https://$NEXUS_USERNAME:$NEXUS_PASSWORD@nexus.mdcatapult.io/repository/pypi-all/pypi"
pip config set global.index-url "https://$NEXUS_USERNAME:$NEXUS_PASSWORD@nexus.mdcatapult.io/repository/pypi-all/simple"
