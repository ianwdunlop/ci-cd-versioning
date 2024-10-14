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
import shutil
import re
import unittest
from unittest import mock

from lib.common import PYPI_USERNAME, PYPI_PASSWORD, CI_TOKEN, CI_COMMIT_BRANCH
from lib.r import release, version, write_version
from helpers import fake_response


class TestR(unittest.TestCase):
    @mock.patch.dict(os.environ, {PYPI_USERNAME: "user", PYPI_PASSWORD: "pass"})
    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.r.write_version')
    @mock.patch('lib.r.git')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_first_release(self, mock_git, mock_requests, _, mock_version_writer):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)
        release([])
        mock_version_writer.assert_any_call("0.0.2.9000", "src")
        mock_version_writer.assert_called_with("0.0.2.9000", "src")

        release(["lib"])
        mock_version_writer.assert_any_call("0.0.2.9000", "lib")
        mock_version_writer.assert_called_with("0.0.2.9000", "lib")

    @mock.patch.dict(os.environ, {PYPI_USERNAME: "user", PYPI_PASSWORD: "pass"})
    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.r.write_version')
    @mock.patch('lib.r.git')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_directory_release(self, mock_git, mock_requests, _, mock_version_writer):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)

        release(["lib"])
        mock_version_writer.assert_any_call("0.0.2.9000", "lib")
        mock_version_writer.assert_called_with("0.0.2.9000", "lib")

    @mock.patch.dict(os.environ, {PYPI_USERNAME: "user", PYPI_PASSWORD: "pass"})
    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.r.write_version')
    @mock.patch('lib.r.git')
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_next_release(self, mock_git, mock_requests, _, mock_version_writer):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.1"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)

        release(["r"])
        mock_version_writer.assert_any_call("0.0.3.9000", "r")
        mock_version_writer.assert_called_with("0.0.3.9000", "r")

    @mock.patch.dict(os.environ, {PYPI_USERNAME: "user", PYPI_PASSWORD: "pass"})
    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-master"})
    @mock.patch("lib.r.write_version")
    @mock.patch("lib.r.git")
    def test_version(self, mock_git, version_writer):
        version("0.0.2", "0.0.2.9000", "dir")
        version_writer.assert_any_call("0.0.2.9000", "dir")
        mock_git.add.assert_any_call("dir/DESCRIPTION")
        mock_git.commit.assert_any_call("-m", 'Setting version to 0.0.2')
        mock_git.push.assert_any_call("origin", "test-master")
        mock_git.tag.assert_any_call("-a", "0.0.2", "-m", 'Setting version to 0.0.2')
        mock_git.push.assert_any_call("origin", "--tags")
        version_writer.assert_any_call("0.0.2.9000", "dir")
        mock_git.commit.assert_any_call("-am", f'Setting version to 0.0.2.9000')
        mock_git.push.assert_any_call("origin", "test-master")

    def test_write_version(self):
        shutil.copyfile('tests/data/DESCRIPTION_EXAMPLE', 'tests/data/DESCRIPTION')
        write_version("0.1.0.9000", "tests/data")
        with open('tests/data/DESCRIPTION', "r") as f:
            content = f.read()
            reg = re.search('(\nVersion: 0.1.0.9000)', content, re.M).group(0)
            self.assertEqual('\nVersion: 0.1.0.9000', reg)

    @classmethod
    def tearDownClass(TestR):
        os.remove('tests/data/DESCRIPTION')

