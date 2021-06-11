import os
from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path):
    repo = tmp_path / "payroll"
    os.mkdir(repo)
    gitdir = repo / ".git"
    os.mkdir(gitdir)
    yield repo
    os.rmdir(gitdir)
    os.rmdir(repo)


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
def gitlog_bad(repo):
    """Had to add some exception handling for a bad datetime
       in requests git log"""
    with open(Path("tests") / "payloads" / "gitlog_bad.txt") as f:
        content = f.read()
    return _clean_data(content)


@pytest.fixture
def gitcommit(repo):
    with open(Path("tests") / "payloads" / "gitcommit.txt") as f:
        content = f.read()
    return _clean_data(content)
