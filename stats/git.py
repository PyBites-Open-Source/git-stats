from collections import namedtuple
from pathlib import Path
import subprocess

from dateutil.parser import parse

from .exceptions import NotAGitRepo

DEFAULT_SINCE = "1 week ago"

Commit = namedtuple("Commit", "hash author date msg")


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
        yield Commit(hash_, author, parse(date), msg)


if __name__ == "__main__":
    repo = "/Users/bbelderbos/code/payroll"
    commits = get_git_log(repo)
    from pprint import pprint as pp
    pp(list(commits))
