from collections import namedtuple, Counter
from pathlib import Path
import re
import subprocess

from dateutil.parser import parse

from .exceptions import NotAGitRepo

DEFAULT_SINCE = "1 week ago"
PY_EXTENSION = ".py"

Commit = namedtuple("Commit", "hash author day msg")
Stats = namedtuple("Stats", "inserts deletes filename")


def get_dotgit_path(repo):
    return Path(repo) / ".git"


def validate_git_dir(repo):
    git_dir = get_dotgit_path(repo)
    if not git_dir.is_dir():
        raise NotAGitRepo(
            (f"{repo} does not have a .git folder "
             "so it does not seem a valid Git repo"))


def get_git_log(repo, since=DEFAULT_SINCE):
    validate_git_dir(repo)

    branches = "--all"
    pretty_format = "%h%x09%an%x09%ad%x09%s"
    cmd = (f"(cd {repo} && git log {branches} "
           f"--pretty=format:'{pretty_format}' "
           f"--since='{since}')")
    output = subprocess.check_output(
        cmd, shell=True).splitlines()

    for line in output:
        fields = line.decode().split("\t")
        hash_, author, date, msg = fields
        day = parse(date).strftime("%Y-%m-%d")
        yield Commit(hash_, author, day, msg)


def get_file_changes(repo, commit, extension=PY_EXTENSION):
    cmd = (f"(cd {repo} && git show --numstat "
           f"{commit} -- '**/*{extension}')")
    output = subprocess.check_output(
        cmd, shell=True).splitlines()

    for line in output:
        m = re.match(r'^(\d+)\t(\d+)\t(\S+)$', line.decode())
        if m:
            inserts, deletes, filename = m.groups()
            yield Stats(int(inserts), int(deletes), filename)


def _get_repo_stats(repo):
    commits = get_git_log(repo)
    for commit in commits:
        for stat in get_file_changes(repo, commit.hash):
            yield commit, stat


def get_repo_stats_by_author(repo):
    stats = Counter()
    for commit, stat in _get_repo_stats(repo):
        stats[commit.author] += stat.inserts + stat.deletes
    return stats


def get_repo_stats_by_day(repo):
    stats = Counter()
    for commit, stat in _get_repo_stats(repo):
        stats[commit.day] += stat.inserts + stat.deletes
    return stats


def get_repo_stats_by_filename(repo):
    stats = Counter()
    for commit, stat in _get_repo_stats(repo):
        stats[stat.filename] += stat.inserts + stat.deletes
    return stats


if __name__ == "__main__":
    repo = "/Users/bbelderbos/code/payroll"
    from pprint import pprint as pp
    #res = get_all_changes_by_day(repo)
    pp(get_repo_stats_by_author(repo))
    pp(get_repo_stats_by_day(repo))
    pp(get_repo_stats_by_filename(repo))
