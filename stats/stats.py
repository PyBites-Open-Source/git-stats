from collections import Counter, defaultdict
from functools import lru_cache

from .git import get_file_changes, get_git_log


class GitStats:

    def __init__(self, extension_pattern=None):
        self.extension_pattern = extension_pattern

    @lru_cache
    def _get_repo_stats(self, repo):
        commits = get_git_log(repo)
        stats = []
        for commit in commits:
            for stat in get_file_changes(
                repo, commit.hash,
                filter_extension=self.extension_pattern
            ):
                stats.append((commit, stat))
        return stats

    def get_number_of_changes_per_week(self, repo):
        stats = Counter()
        for commit, stat in self._get_repo_stats(repo):
            stats[commit.week] += stat.inserts + stat.deletes
        return stats

    def get_number_of_commits_per_week_and_author(self, repo):
        stats = defaultdict(lambda: defaultdict(set))
        for commit, _ in self._get_repo_stats(repo):
            stats[commit.week][commit.author].add(commit.hash)
        return stats

    def get_most_changed_files(self, repo, number_of_files=10):
        """Amount of times a filename was part of a commit
        (independent of the size of the commit)
        TODO: could make this weighted
        TODO: might want to take into account last N commits
                because already found a usecase of __init__.py
                before refactoring (so should not count)
        """
        stats = Counter()
        for _, stat in self._get_repo_stats(repo):
            stats[stat.filename] += 1
        return stats.most_common(number_of_files)
