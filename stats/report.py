import os

import numpy as np
from uniplot import plot

from .stats import GitStats


def _create_header():
    header = "< Git Repo Activity Report"
    header += " >"
    return header


def show_report(repo):
    gstats = GitStats(repo)

    sep = "-" * 50
    print(sep)

    header = _create_header()
    print(header)

    print(f"> Repo: {os.path.basename(repo)}")
    print(sep)

    daily_progress = gstats.get_number_of_changes_per_day()
    x, y = zip(*daily_progress)
    breakpoint()
    title = "Repo changes (inserts and deletes) over time"
    plot(y, x, title=title)

    weekly_changes = gstats.get_number_of_changes_per_week()
    print("\n* Repo changes (inserts and deletes) per week:\n")
    for week, changes in sorted(weekly_changes):
        print(f"{week:<38} | {changes:>3}")

    print("\n* Number of commits per week and author:\n")
    commits = gstats.get_number_of_commits_per_week_and_author()
    for week, commits_cnt in sorted(commits):
        print(week)
        for author, author_commits in commits_cnt.items():
            print(f"- {author:<36} | {len(author_commits):>3}")

    print("\n* Files that are most often found in commits:\n")
    for file, times_seen in gstats.get_most_changed_files():
        print(f"{file:<38} | {times_seen:>3}")

    print(sep)
