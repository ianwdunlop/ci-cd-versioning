import os
from unittest import mock
from lib.common import NEXUS_USERNAME, NEXUS_PASSWORD, CI_TOKEN, CI_COMMIT_BRANCH, PACKAGE_PASSWORD
from lib.python import config_pip, release, version
from helpers import fake_response


class TestPython:
    @mock.patch.dict(os.environ, {PACKAGE_PASSWORD: "true", NEXUS_USERNAME: "user", NEXUS_PASSWORD: "pass"})
    @mock.patch("lib.python.check_call")
    def test_config_pip(self, mock_call):
        config_pip()
        mock_call.assert_any_call(["pip", "config", "set", "global.index",
                                   "https://user:pass@nexus.wopr.inf.mdc/repository/pypi-all/pypi"])
        mock_call.assert_any_call(["pip", "config", "set", "global.index-url",
                                   "https://user:pass@nexus.wopr.inf.mdc/repository/pypi-all/simple"])
        mock_call.assert_any_call(["pip", "config", "set", "global.trusted-host", "nexus.wopr.inf.mdc"])

    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.python.write_version')
    @mock.patch('lib.python.git')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_release(self, mock_git, mock_requests, _, mock_version_writer):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)
        release([])
        mock_version_writer.assert_any_call("0.0.1", "src")
        mock_version_writer.assert_called_with("0.0.2a0", "src")


        release(["lib"])
        mock_version_writer.assert_any_call("0.0.1", "lib")
        mock_version_writer.assert_called_with("0.0.2a0", "lib")

    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-master"})
    @mock.patch("lib.python.write_version")
    @mock.patch("lib.python.git")
    def test_version(self, mock_git, version_writer):
        version("0.0.0", "0.0.1a0", "dir")
        version_writer.assert_any_call("0.0.0", "dir")
        mock_git.add.assert_any_call("dir/version.py")
        mock_git.commit.assert_any_call("-m", 'Setting version to 0.0.0')
        mock_git.push.assert_any_call("origin", "test-master")
        mock_git.tag.assert_any_call("-a", "0.0.0", "-m", 'Setting version to 0.0.0')
        mock_git.push.assert_any_call("origin", "--tags")
        version_writer.assert_any_call("0.0.1a0", "dir")
        mock_git.commit.assert_any_call("-am", f'Setting version to 0.0.1a0')
        mock_git.push.assert_any_call("origin", "test-master")

    def test_write_version(self):
        pass
