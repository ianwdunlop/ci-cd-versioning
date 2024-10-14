#  Copyright 2024 Medicines Discovery Catapult
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from unittest import mock
from lib.common import PYPI_USERNAME, PYPI_PASSWORD, CI_TOKEN, CI_COMMIT_BRANCH, PACKAGE_PASSWORD
from lib.python import config_pip, release, version
from helpers import fake_response


class TestPython:
    @mock.patch.dict(os.environ, {PACKAGE_PASSWORD: "true", PYPI_USERNAME: "user", PYPI_PASSWORD: "pass"})
    @mock.patch("lib.python.check_call")
    def test_config_pip(self, mock_call):
        config_pip()
        mock_call.assert_any_call(["pip", "config", "set", "global.index",
                                   "https://user:pass@pypi.org/repository/pypi-all/pypi"])
        mock_call.assert_any_call(["pip", "config", "set", "global.index-url",
                                   "https://user:pass@pypi.org/repository/pypi-all/simple"])
        mock_call.assert_any_call(["pip", "config", "set", "global.trusted-host", "pypi.org"])

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
