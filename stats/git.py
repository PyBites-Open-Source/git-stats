from collections import namedtuple
from datetime import datetime
from pathlib import Path
import re
import sys

from .exceptions import NotAGitRepo
from .utils import run_command

Commit = namedtuple("Commit", "hash author date week msg")
Stats = namedtuple("Stats", "inserts deletes filename")


def validate_git_dir(repo):
    git_dir = Path(repo) / ".git"
    if not git_dir.is_dir():
        raise NotAGitRepo(
            (f"{repo} does not have a .git folder "
             "so it does not seem a valid Git repo"))


def _create_log_command(repo, since):
    parts = [
        "(", "cd ", repo, " && ", "git log ",
        "--all ", "--pretty=format:'",
        "%h%x09%an%x09%ad%x09%s", "'"]
    if since is not None:
        parts.extend(
            [" --since='", since, "'"])
    parts.append(")")
    return "".join(parts)


def get_git_log(repo, since=None):
    if isinstance(repo, Path):
        repo = str(repo)

    validate_git_dir(repo)

    cmd = _create_log_command(repo, since)
    output = run_command(cmd)

    for line in output:
        fields = line.decode().split("\t")
        hash_, author, date, msg = fields
        try:
            dt = datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z")
        except ValueError as exc:
            print((f"Skipping commit {hash_} because cannot convert "
                   f"{date} to datetime, exception: {exc}"),
                  file=sys.stderr)
            continue
        week = dt.strftime("%Y-%W")
        yield Commit(hash_, author, dt, week, msg)


def get_file_changes(repo, commit):
    cmd = f"(cd {repo} && git show --numstat {commit})"
    output = run_command(cmd)

    for line in output:
        m = re.match(r'^(\d+)\t(\d+)\t(\S+)$', line.decode())
        if m:
            inserts, deletes, filename = m.groups()
            yield Stats(int(inserts), int(deletes), filename)
