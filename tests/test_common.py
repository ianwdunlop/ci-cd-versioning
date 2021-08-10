from lib.common import (
    get_ci_token,
    latest_tag,
    increment,
    parse_common_flags,
    env,
    next_tag,
    git_log,
    rebase,
    get_rebase_branch,
    REBASE_BRANCH,
    UPLOADS,
    LATEST_TAG,
    BUMP,
    GIT_LOG,
    NEXT_TAG,
    CI_TOKEN
)
import os
from unittest import mock
import pytest

class UnexpectedArgumentException(Exception):
    pass


class TestCommon:

    @mock.patch.dict(os.environ, {CI_TOKEN: "test_token"})
    def test_get_ci_token(self):
        try:
            get_ci_token()
        except EnvironmentError as e:
            assert str(e) == "Missing environment variable CI_TOKEN"

        token = get_ci_token()
        assert token == "test_token"

    @mock.patch('lib.common.git')
    def test_latest_tag(self, mock_git):
        latest_tag()
        mock_git.describe.assert_called_once_with("--abbrev=0")

    @mock.patch('lib.common.git')
    def test_increment(self, mock_git):
        def new_mock_log(returns, tag):
            def mock_log(*args) -> str:
                true_args = ["--no-merges", '--pretty=format:%s', f"{tag}..HEAD"]
                log = None
                for i, arg in enumerate(args):
                    if arg != true_args[i]:
                        break
                    if i == len(true_args) - 1:
                        log = returns

                true_args = ["--merges", "--oneline", f"{tag}..HEAD"]
                for i, arg in enumerate(args):
                    if arg != true_args[i]:
                        break
                    if i == len(true_args) - 1:
                        log = returns

                if not log:
                    raise UnexpectedArgumentException("?")

                return log

            return mock_log

        mock_git.log.side_effect = new_mock_log("hello", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "patch"

        mock_git.log.side_effect = new_mock_log("breaking-change/", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "major"

        mock_git.log.side_effect = new_mock_log("breaking-change:", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "major"

        mock_git.log.side_effect = new_mock_log("major/", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "major"

        mock_git.log.side_effect = new_mock_log("major:", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "major"

        mock_git.log.side_effect = new_mock_log("feature/", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "minor"

        mock_git.log.side_effect = new_mock_log("feature:", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "minor"

        mock_git.log.side_effect = new_mock_log("minor/", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "minor"

        mock_git.log.side_effect = new_mock_log("minor:", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "minor"

    def test_parse_common_flags(self):
        e = parse_common_flags(["-r", "hello", "-u", "./*"])
        assert e[REBASE_BRANCH] == "hello"
        assert e[UPLOADS] == "./*"

    @mock.patch('lib.common.git')
    def test_env(self, mock_git):
        def log(*args):
            return "hello"

        def describe(*args):
            return "0.0.0"

        mock_git.log.side_effect = log
        mock_git.describe.side_effect = describe
        e = env([])
        assert e[LATEST_TAG] == "0.0.0"
        assert e[BUMP] == 'patch'
        assert e[NEXT_TAG] == "0.0.1"
        assert e[GIT_LOG] == 'hello'

    def test_next_tag(self):
        tag = next_tag("", "patch")
        assert tag == "0.0.1"

        tag = next_tag("", "minor")
        assert tag == "0.0.1"

        tag = next_tag("", "major")
        assert tag == "0.0.1"

        tag = next_tag("0.0.0", "patch")
        assert tag == "0.0.1"

        tag = next_tag("0.0.0", "minor")
        assert tag == "0.1.0"

        tag = next_tag("0.0.0", "major")
        assert tag == "1.0.0"

        with pytest.raises(ValueError):
            next_tag("0.0.0", "not a real increment")

    @mock.patch('lib.common.git')
    def test_git_log(self, mock_git):
        def log(*args):
            return """"<'>&'"""
        mock_git.log.side_effect = log
        test_log = git_log("0.0.0")
        # TODO: The backslashes shouldn't be in this. Python is escaping the single quotes.
        # The backslashes aren't in the true output.
        assert test_log == """&quot;&lt;\\&#39;&gt;&amp;\\"""

    @mock.patch.dict(os.environ, {REBASE_BRANCH: "test-develop"})
    @mock.patch('lib.common.git')
    @mock.patch('lib.common.ci_commit_branch', new="test-master")
    def test_rebase(self, mock_git):
        rebase()
        mock_git.checkout.assert_called_with("test-develop")
        mock_git.rebase.assert_called_with("test-master")
        mock_git.push.assert_called_with("origin", "test-develop")

    @mock.patch('lib.common.git')
    def test_get_rebase_branch(self, mock_git):
        from git.exc import GitCommandError

        def show_ref_0(*args):
            pass

        mock_git.show_ref.side_effect = show_ref_0
        branch = get_rebase_branch()
        assert branch == "develop"

        def show_ref_1(*args):
            if args[2] == "refs/remotes/origin/develop":
                raise GitCommandError("shows that develop is skipped if it doesn't exist")

        mock_git.show_ref.side_effect = show_ref_1
        branch = get_rebase_branch()
        assert branch == "dev"

        def show_ref_2(*args):
            if args[2] == "refs/remotes/origin/develop" or args[2] == "refs/remotes/origin/dev":
                raise GitCommandError("shows that both dev and develop are skipped if it doesn't exist")

        mock_git.show_ref.side_effect = show_ref_2
        branch = get_rebase_branch()
        assert branch == ""

    @mock.patch('lib.common.git')
    def test_release(self, mock_git):
        pass

    def test_config_git(self):
        pass

    def test_create_attachment(self):
        pass

    def test_version(self):
        pass

    def test_short_sha(self):
        pass
