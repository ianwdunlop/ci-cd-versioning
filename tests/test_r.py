import os
import shutil
import re
import unittest
from unittest import mock

from lib.common import NEXUS_USERNAME, NEXUS_PASSWORD, CI_TOKEN, CI_COMMIT_BRANCH
from lib.r import release, version, write_version
from helpers import fake_response


class TestR(unittest.TestCase):
    @mock.patch.dict(os.environ, {NEXUS_USERNAME: "user", NEXUS_PASSWORD: "pass"})
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
        mock_version_writer.assert_any_call("0.0.2a0", "src")
        mock_version_writer.assert_called_with("0.0.2a0", "src")

        release(["lib"])
        mock_version_writer.assert_any_call("0.0.2a0", "lib")
        mock_version_writer.assert_called_with("0.0.2a0", "lib")

    @mock.patch.dict(os.environ, {NEXUS_USERNAME: "user", NEXUS_PASSWORD: "pass"})
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
        mock_version_writer.assert_any_call("0.0.2a0", "lib")
        mock_version_writer.assert_called_with("0.0.2a0", "lib")

    @mock.patch.dict(os.environ, {NEXUS_USERNAME: "user", NEXUS_PASSWORD: "pass"})
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
        mock_version_writer.assert_any_call("0.0.3a0", "r")
        mock_version_writer.assert_called_with("0.0.3a0", "r")

    @mock.patch.dict(os.environ, {NEXUS_USERNAME: "user", NEXUS_PASSWORD: "pass"})
    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-master"})
    @mock.patch("lib.r.write_version")
    @mock.patch("lib.r.git")
    def test_version(self, mock_git, version_writer):
        version("0.0.2", "0.0.2a0", "dir")
        version_writer.assert_any_call("0.0.2a0", "dir")
        mock_git.add.assert_any_call("dir/DESCRIPTION")
        mock_git.commit.assert_any_call("-m", 'Setting version to 0.0.2')
        mock_git.push.assert_any_call("origin", "test-master")
        mock_git.tag.assert_any_call("-a", "0.0.2", "-m", 'Setting version to 0.0.2')
        mock_git.push.assert_any_call("origin", "--tags")
        version_writer.assert_any_call("0.0.2a0", "dir")
        mock_git.commit.assert_any_call("-am", f'Setting version to 0.0.2a0')
        mock_git.push.assert_any_call("origin", "test-master")

    def test_write_version(self):
        shutil.copyfile('tests/data/DESCRIPTION_EXAMPLE', 'tests/data/DESCRIPTION')
        write_version("0.1.0a0", "tests/data")
        with open('tests/data/DESCRIPTION', "r") as f:
            content = f.read()
            reg = re.search('(Version: 0.1.0a0)', content, re.M).group(0)
            self.assertEqual('Version: 0.1.0a0', reg)

    @classmethod
    def tearDownClass(TestR):
        os.remove('tests/data/DESCRIPTION')

