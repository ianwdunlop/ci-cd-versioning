from unittest import mock
from lib.golang import env, GOPRIVATE, release, netrc_file
from lib.common import NEXT_TAG, GIT_LOG, BUMP, LATEST_TAG, UPLOADS, REBASE_BRANCH, CI_SERVER_HOST, CI_SERVER_PORT, CI_TOKEN, CI_READONLY_TOKEN, CI_READONLY_USER
from helpers import fake_response
import os


class TestGolang:

    @mock.patch.dict(os.environ, {CI_SERVER_HOST: "gitlab.example.com", CI_SERVER_PORT: "443"})
    @mock.patch("lib.common.git")
    def test_env(self, mock_git):
        mock_git.describe.side_effect = lambda x, y: "v0.0.0"
        mock_git.log.side_effect = lambda x, y, z: "hello"
        e = env([])
        assert e[NEXT_TAG] == "v0.0.1"
        assert e[GOPRIVATE] == "gitlab.example.com:443/*"
        assert e[GIT_LOG] == "hello"
        assert e[BUMP] == "patch"
        assert e[LATEST_TAG] == "v0.0.0"
        assert e[UPLOADS] == ""
        assert e[REBASE_BRANCH] == ""

    @mock.patch.dict(os.environ, {CI_TOKEN: "token"})
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.git')
    def test_release(self, mock_git, mock_requests):
        def log(*args):
            return ""

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        mock_requests.post.side_effect = fake_response(200)
        release([])

    @mock.patch.dict(os.environ, {CI_READONLY_TOKEN: "daves-token", CI_READONLY_USER: "dave", CI_SERVER_HOST: "gitlab.example.com"})
    def test_netrc(self):
        netrc = netrc_file()
        assert netrc == "\nmachine gitlab.example.com\n\tlogin dave\n\tpassword daves-token"