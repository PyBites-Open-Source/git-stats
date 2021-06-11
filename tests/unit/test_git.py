from unittest.mock import patch

import pytest

from stats.git import (validate_git_dir, _create_log_command,
                       get_git_log, get_file_changes,
                       Commit, Stats)
from stats.exceptions import NotAGitRepo


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
        week='2021-22', msg='ran isort')
    assert last == Commit(
        hash='0fe8891', author='Bob Belderbos',
        week='2021-21', msg="backup commit'")


@patch('subprocess.check_output')
def test_handling_bad_datetime(subprocess_mock, repo, gitlog_bad, capfd):
    subprocess_mock.return_value = gitlog_bad
    commits = list(get_git_log(str(repo)))
    assert len(commits) == 0
    actual_stderr = capfd.readouterr()[1].strip()
    expected_stderr = (
        "Skipping commit '5e6ecdad because cannot convert "
        "Thu Sep 8 02:38:50 2011 +51800 to datetime, "
        "exception: time data 'Thu Sep 8 02:38:50 2011 +51800' "
        "does not match format '%a %b %d %H:%M:%S %Y %z'"
    )
    assert actual_stderr == expected_stderr


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
