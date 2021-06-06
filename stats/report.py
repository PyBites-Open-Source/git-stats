import os

from .git import GitStats


def show_report(repo, extension_pattern=None):
    gstats = GitStats(extension_pattern)

    sep = "-" * 50
    print(sep)
    print("< Git Repo Activity Report (Python files only) >")
    print(f"> Repo: {os.path.basename(repo)}")
    print(sep)

    print("\n* Repo inserts and deletes per day:\n")
    for day, changes in sorted(
        gstats.get_number_of_changes_per_day(repo).items()
    ):
        print(f"{day:<38} | {changes:>3}")

    print("\n* Number of commits per day and author:\n")
    commits = gstats.get_number_of_commits_per_day_and_author(repo)
    for day, commits_cnt in sorted(commits.items()):
        print(day)
        for author, author_commits in commits_cnt.items():
            print(f"- {author:<36} | {len(author_commits):>3}")

    print("\n* Files that are most often found in commits:\n")
    for file, times_seen in gstats.get_most_changed_files(repo):
        print(f"{file:<38} | {times_seen:>3}")

    print(sep)
