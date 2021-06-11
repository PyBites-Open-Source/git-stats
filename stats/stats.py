from collections import Counter, defaultdict

from tqdm import tqdm

from .git import get_file_changes, get_git_log


class GitStats:

    def __init__(self, repo):
        self.repo = repo
        self.repo_stats = self._get_repo_stats()

    def _get_repo_stats(self):
        commits = list(get_git_log(self.repo))
        stats = []
        for commit in tqdm(commits, total=len(commits)):
            for stat in get_file_changes(self.repo, commit.hash):
                stats.append((commit, stat))
        return stats

    def get_number_of_changes_per_week(self):
        stats = Counter()
        for commit, stat in self.repo_stats:
            stats[commit.week] += stat.inserts + stat.deletes
        return stats.items()

    def get_number_of_commits_per_week_and_author(self):
        stats = defaultdict(lambda: defaultdict(set))
        for commit, _ in self.repo_stats:
            stats[commit.week][commit.author].add(commit.hash)
        return stats.items()

    def get_most_changed_files(self, number_of_files=10):
        """Amount of times a filename was part of a commit
        (independent of the size of the commit)
        TODO: could make this weighted
        TODO: might want to take into account last N commits
                because already found a usecase of __init__.py
                before refactoring (so should not count)
        """
        stats = Counter()
        for _, stat in self.repo_stats:
            stats[stat.filename] += 1
        return stats.most_common(number_of_files)
