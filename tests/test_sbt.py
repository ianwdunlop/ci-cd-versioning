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
from lib.common import CI_TOKEN
from lib.sbt import release, version
from helpers import fake_response


class TestSbt:
    @mock.patch('lib.sbt.check_call')
    def test_version(self, mock_call):
        version("0.0.0", "0.0.1-SNAPSHOT")
        mock_call.assert_called_with(["sbt", f'release with-defaults release-version 0.0.0 next-version 0.0.1-SNAPSHOT'])

    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.sbt.version')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_release(self, mock_git, mock_requests, mock_version):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)
        release([])
        mock_version.assert_called_with("0.0.1", "0.0.2-SNAPSHOT")
