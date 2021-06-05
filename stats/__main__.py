from pprint import pprint as pp
import sys

from .git import (get_number_of_changes_per_day,
                  get_number_of_commits_per_day_and_author,
                  get_most_changed_files)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} YOUR_REPO_FOLDER")
        sys.exit(1)

    repo = sys.argv[1]

    print("Git Repo Activity Report (Python files only)")
    print("\nRepo inserts and deletes per day:")
    pp(sorted(get_number_of_changes_per_day(repo).items()))
    print("\nNumber of commits per day and author:")
    pp(get_number_of_commits_per_day_and_author(repo))
    print("\nTop 10 files most often found in commits:")
    pp(get_most_changed_files(repo))


if __name__ == "__main__":
    main()
