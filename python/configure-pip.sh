#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# shellcheck source=.
. "$DIR/utils.sh"

pip config set global.trusted-host "nexus.wopr.inf.mdc pypi.org files.pythonhosted.org"
reportError $?

pip config set global.index "https://$NEXUS_USERNAME:$NEXUS_PASSWORD@nexus.mdcatapult.io/repository/pypi-all/pypi"
reportError $?

pip config set global.index-url "https://$NEXUS_USERNAME:$NEXUS_PASSWORD@nexus.mdcatapult.io/repository/pypi-all/simple"
reportError $?
