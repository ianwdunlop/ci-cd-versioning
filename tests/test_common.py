import os
from lib.common import (
    ci_token,
    fetch_all_and_checkout_latest,
    latest_tag,
    increment,
    parse_common_flags,
    env,
    next_tag,
    git_log,
    rebase,
    get_rebase_branch,
    set_git_config,
    release,
    create_release,
    create_attachment,
    version,
    short_sha,
    REBASE_BRANCH,
    UPLOADS,
    LATEST_TAG,
    BUMP,
    GIT_LOG,
    NEXT_TAG,
    CI_TOKEN,
    CI_PROJECT_ID,
    CI_API_V4_URL,
    CI_PROJECT_PATH,
    CI_SERVER_HOST,
    CI_COMMIT_BRANCH,
    CI_DOMAIN
)
from unittest import mock
import pytest
from requests.models import HTTPError
from helpers import fake_response

class UnexpectedArgumentException(Exception):
    pass


class TestCommon:

    @mock.patch.dict(os.environ, {CI_TOKEN: "test_token"})
    def test_get_ci_token(self):
        try:
            ci_token()
        except EnvironmentError as e:
            assert str(e) == "Missing environment variable CI_TOKEN"

        token = ci_token()
        assert token == "test_token"

    @mock.patch('lib.common.git')
    def test_latest_tag(self, mock_git):
        mock_git.rev_list.side_effect = lambda x,y : 'oraoianroin'
        latest_tag()
        mock_git.rev_list.assert_called_once_with("--tags", "--max-count=1")
        mock_git.describe.assert_called_once_with("--tags", "oraoianroin")

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
                    raise UnexpectedArgumentException(str(args))

                return log

            return mock_log

        mock_git.log.side_effect = new_mock_log("hello", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "patch"

        mock_git.log.side_effect = new_mock_log("breaking-change/", "0.0.0")
        inc = increment("0.0.0")
        assert inc == "major"

        mock_git.log.side_effect = new_mock_log("Merge branch 'breaking-change/1234/something' into 'develop'", "0.0.0")
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

        mock_git.log.side_effect = new_mock_log("Merge branch 'feature/1234/something' into 'develop'", "0.0.0")
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

    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-master"})
    @mock.patch('lib.common.git')
    def test_rebase(self, mock_git):
        rebase("test-develop")
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

    @mock.patch.dict(os.environ, {CI_TOKEN: "test-token", CI_PROJECT_ID: "1",
                                  CI_SERVER_HOST: "gitlab.example.com", CI_PROJECT_PATH: "project/path",
                                  CI_COMMIT_BRANCH: "test-develop", CI_DOMAIN: "example.com"}, clear = True)
    @mock.patch("lib.common.git")
    def test_set_git_config(self, mock_git):
        set_git_config()
        mock_git.remote.assert_called_with("set-url", "origin", "https://project_1_bot:test-token@gitlab.example.com/project/path.git")
        mock_git.config.assert_any_call("user.name", "project_1_bot")
        mock_git.config.assert_called_with("user.email", "project1_bot@example.com")

    @mock.patch.dict(os.environ, {CI_TOKEN: "test-token", CI_PROJECT_ID: "1",
                                  CI_SERVER_HOST: "gitlab.example.com", CI_PROJECT_PATH: "project/path",
                                  CI_COMMIT_BRANCH: "test-develop"}, clear = True)
    @mock.patch("lib.common.git")
    def test_default_email_config(self, mock_git):
        set_git_config()
        mock_git.remote.assert_called_with("set-url", "origin", "https://project_1_bot:test-token@gitlab.example.com/project/path.git")
        mock_git.config.assert_any_call("user.name", "project_1_bot")
        mock_git.config.assert_called_with("user.email", "project1_bot@gitlab.mdcatapult.io")

    @mock.patch.dict(os.environ, {CI_COMMIT_BRANCH: "test-develop"})
    @mock.patch("lib.common.git")
    def test_fetch_all_and_checkout_latest(self, mock_git):
        fetch_all_and_checkout_latest()
        mock_git.fetch.assert_called_with("--all", "--tags")
        mock_git.checkout.assert_called_with("test-develop")
        mock_git.pull.assert_called_with("origin", "test-develop")


    @mock.patch.dict(os.environ, {CI_TOKEN: "test-token", CI_PROJECT_ID: "1", CI_API_V4_URL: "https://gitlab.example.com/api/v4"})
    @mock.patch('lib.common.requests')
    def test_create_release(self, mock_requests):
        mock_requests.post.side_effect = fake_response(200)
        create_release("0.0.0", "afawef my log<br/>fw44g53 my second log")
        mock_requests.post.assert_called_with("https://gitlab.example.com/api/v4/projects/1/releases",
                                                       json={"name": "0.0.0", "tag_name": "0.0.0", "description": "## Changelog\n\nafawef my log<br/>fw44g53 my second log"},
                                                       headers={"PRIVATE-TOKEN": "test-token",  'Content-Type': 'application/json'})

        mock_requests.post.side_effect = fake_response(400)
        with pytest.raises(HTTPError):
            create_release("0.0.0", "my log")

    @mock.patch.dict(os.environ, {CI_TOKEN: "test-token", CI_PROJECT_ID: "1", CI_API_V4_URL: "https://gitlab.example.com/api/v4", CI_SERVER_HOST: "gitlab.example.com"})
    @mock.patch('lib.common.requests')
    @mock.patch('lib.common.glob')
    @mock.patch('builtins.open', read_data="data")
    def test_create_attachment(self, mock_open, mock_glob, mock_requests):
        def glob(*args, **kwargs):
            return ["my-upload.txt"]
        mock_requests.post.side_effect = fake_response(200, {
            "alt": "my-upload",
            "url": "/uploads/66dbcd21ec5d24ed6ea225176098d52b/my-upload.txt",
            "full_path": "/namespace1/project1/uploads/66dbcd21ec5d24ed6ea225176098d52b/my-upload.txt",
            "markdown": "![my-upload](/uploads/66dbcd21ec5d24ed6ea225176098d52b/my-upload.txt)"
        })
        mock_glob.glob.side_effect = glob
        create_attachment("*", "0.0.0")
        mock_glob.glob.assert_called_with("*", recursive=True)
        mock_open.assert_called_with("my-upload.txt", "rb")
        mock_requests.post.assert_called_with("https://gitlab.example.com/api/v4/projects/1/releases/0.0.0/assets/links",
                                                       data={"name": "my-upload.txt", "url": "https://gitlab.example.com/namespace1/project1/uploads/66dbcd21ec5d24ed6ea225176098d52b/my-upload.txt"},
                                                       headers={"PRIVATE-TOKEN": "test-token"})

    @mock.patch.dict(os.environ, {CI_TOKEN: "test-token", CI_COMMIT_BRANCH: "test-master"})
    @mock.patch("lib.common.git")
    def test_version(self, mock_git):
        version("0.0.0")
        mock_git.commit.assert_called_with("--allow-empty", "-am", 'Setting version to 0.0.0')
        mock_git.push.assert_any_call("origin", "test-master")
        mock_git.tag.assert_called_with("-a", "0.0.0", "-m", 'Setting version to 0.0.0')
        mock_git.push.assert_called_with("origin", "--tags")

    @mock.patch("lib.common.git")
    def test_short_sha(self, mock_git):
        short_sha()
        mock_git.rev_parse.assert_called_once_with("--short", "HEAD")
