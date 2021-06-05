import sys

from .report import show_report


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} YOUR_REPO_FOLDER")
        sys.exit(1)

    repo = sys.argv[1]
    show_report(repo)


if __name__ == "__main__":
    main()
