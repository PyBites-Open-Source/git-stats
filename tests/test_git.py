from unittest.mock import patch
import os
from pathlib import Path

import pytest

from stats.git import (validate_git_dir, _create_log_command,
                       get_git_log, get_file_changes,
                       Commit, Stats)
from stats.exceptions import NotAGitRepo


@pytest.fixture
def repo(tmp_path):
    repo = tmp_path / "payroll"
    os.mkdir(repo)
    gitdir = repo / ".git"
    os.mkdir(gitdir)
    return repo


def _clean_data(content):
    lines = [line.lstrip("b").rstrip("\n").encode()
             for line in content.replace("\\t", "\t").split("\\n")]
    return b'\n'.join(lines)


@pytest.fixture
def gitlog(repo):
    """Preparing the output exactly as subprocess / git log
       would output it, so we don't have to use a real git
       repository (dependency)"""
    with open(Path("tests") / "payloads" / "gitlog.txt") as f:
        content = f.read()
    return _clean_data(content)


@pytest.fixture
def gitcommit(repo):
    with open(Path("tests") / "payloads" / "gitcommit.txt") as f:
        content = f.read()
    return _clean_data(content)


def test_validate_git_dir(tmp_path):
    with pytest.raises(NotAGitRepo):
        validate_git_dir(tmp_path)


@pytest.mark.parametrize("since", [None, "1 week ago"])
def test_create_log_command(repo, since):
    actual = _create_log_command(str(repo), since)
    expected = (f"(cd {repo} && git log --all "
                "--pretty=format:'%h%x09%an%x09%ad%x09%s'")
    if since is not None:
        expected += " --since='1 week ago'"
    expected += ")"
    assert actual == expected


@patch('subprocess.check_output')
def test_get_git_log(subprocess_mock, repo, gitlog):
    subprocess_mock.return_value = gitlog
    commits = list(get_git_log(str(repo)))
    assert len(commits) == 34
    assert all(type(co) is Commit for co in commits)
    first, *_, last = commits
    assert first == Commit(
        hash="'1f86432", author='Bob Belderbos',
        day='2021-06-02', msg='ran isort')
    assert last == Commit(
        hash='0fe8891', author='Bob Belderbos',
        day='2021-05-30', msg="backup commit'")


@patch('subprocess.check_output')
def test_get_file_changes(subprocess_mock, repo, gitcommit):
    subprocess_mock.return_value = gitcommit
    stats = list(get_file_changes(repo, "abc123"))
    assert stats == [
        Stats(inserts=1, deletes=1, filename='payroll/company.py'),
        Stats(inserts=1, deletes=1, filename='payroll/employee.py'),
        Stats(inserts=1, deletes=1, filename='payroll/payment.py'),
        Stats(inserts=1, deletes=1, filename='payroll/payroll.py'),
        Stats(inserts=1, deletes=1, filename='payroll/timesheet.py'),
        Stats(inserts=1, deletes=4, filename='tests/conftest.py'),
        Stats(inserts=1, deletes=2, filename='tests/test_objects.py')
    ]
