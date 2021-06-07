# Are you an active developer?

The aim of this package is to get some useful stats from a local `git` repo.

## To run it

All code uses Standard Library so far so you should be able to run it upon checkout:

```
python3 -m stats YOUR_REPO_FOLDER
```

## Example output

Bit meta but here is how it looks for this repo at this time of writing:

```
$ python3 -m stats ~/code/git-stats
--------------------------------------------------
< Git Repo Activity Report >
> Repo: git-stats
--------------------------------------------------

* Repo inserts and deletes per week:

2021-22                                | 1607
2021-23                                | 479

* Number of commits per week and author:

2021-22
- Bob Belderbos                        |  32
2021-23
- Bob Belderbos                        |   3

* Files that are most often found in commits:

stats/git.py                           |  16
stats/report.py                        |   9
tests/functional/test_report.py        |   6
README.md                              |   5
tests/conftest.py                      |   4
stats/stats.py                         |   3
Makefile                               |   3
stats/__main__.py                      |   3
tests/unit/test_git.py                 |   2
tests/test_git.py                      |   2
--------------------------------------------------
```

## To run the tests:

There are unit tests and one functional (end-to-end) test. You can run them like this:

```
make venv
source venv/bin/activate
make install
make unit (or make test)
make functional
make testall
make coverage
```
