from collections import Counter, defaultdict, namedtuple
from functools import lru_cache
from pathlib import Path
import re

from dateutil.parser import parse

from .exceptions import NotAGitRepo
from .utils import run_command

PY_EXTENSION = ".py"

Commit = namedtuple("Commit", "hash author day msg")
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
        day = parse(date).strftime("%Y-%m-%d")
        yield Commit(hash_, author, day, msg)


def get_file_changes(repo, commit,
                     filter_extension=PY_EXTENSION):
    cmd = (f"(cd {repo} && git show --numstat "
           f"{commit} -- '**/*{filter_extension}')")
    output = run_command(cmd)

    for line in output:
        m = re.match(r'^(\d+)\t(\d+)\t(\S+)$', line.decode())
        if m:
            inserts, deletes, filename = m.groups()
            yield Stats(int(inserts), int(deletes), filename)


@lru_cache
def _get_repo_stats(repo):
    commits = get_git_log(repo)
    stats = []
    for commit in commits:
        for stat in get_file_changes(repo, commit.hash):
            stats.append((commit, stat))
    return stats


def get_number_of_changes_per_day(repo):
    stats = Counter()
    for commit, stat in _get_repo_stats(repo):
        stats[commit.day] += stat.inserts + stat.deletes
    return stats


def get_number_of_commits_per_day_and_author(repo):
    stats = defaultdict(lambda: Counter())
    for commit, _ in _get_repo_stats(repo):
        stats[commit.day][commit.author] += 1
    return stats


def get_most_changed_files(repo, number_of_files=10):
    """Amount of times a filename was part of a commit
       (independent of the size of the commit)
       TODO: could make this weighted
       TODO: might want to take into account last N commits
             because already found a usecase of __init__.py
             before refactoring (so should not count)
    """
    stats = Counter()
    for _, stat in _get_repo_stats(repo):
        stats[stat.filename] += 1
    return stats.most_common(number_of_files)
