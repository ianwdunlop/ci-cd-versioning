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

from unittest import mock
import os
from lib.common import CI_TOKEN, CI_COMMIT_BRANCH
from lib.node import release, version
from helpers import fake_response


class TestNode:

    @mock.patch.dict(os.environ, {CI_TOKEN: "token", CI_COMMIT_BRANCH: "test-master"})
    @mock.patch('lib.node.git')
    @mock.patch('lib.node.check_call')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_release(self, mock_git, mock_requests, mock_call, mock_node_git):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)
        release([])
        mock_call.assert_called_once_with(["npm", '--no-git-tag-version', 'version', "0.0.1"])
        mock_node_git.push.assert_any_call("origin", "test-master")
        mock_node_git.push.assert_called_with("origin", "--tags")

    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-master"})
    @mock.patch('lib.node.check_call')
    @mock.patch('lib.node.git')
    def test_version(self, mock_git, mock_call):
        version("major")
        mock_call.assert_called_once_with(['npm', '--no-git-tag-version', 'version', 'major'])
        mock_git.push.assert_any_call("origin", "test-master")
        mock_git.push.assert_called_with("origin", "--tags")