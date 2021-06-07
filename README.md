# Are you an active developer?

The aim of this package is to get some useful stats from a local `git` repo.

## To run it:

```
make venv
source venv/bin/activate
make install
python -m stats YOUR_REPO_FOLDER
```

## Example output:

```
--------------------------------------------------
< Git Repo Activity Report >
> Repo: payroll
--------------------------------------------------

* Repo inserts and deletes per week:

2021-21                                | 1116
# Are you an active developer?
2021-22                                | 192

* Number of commits per week and author:

2021-21
- Bob Belderbos                        |  19
2021-22
- Bob Belderbos                        |  16

* Files that are most often found in commits:

payroll/payroll.py                     |  12
tests/conftest.py                      |  10
payroll/timesheet.py                   |   9
tests/test_objects.py                  |   9
payroll/employee.py                    |   8
README.md                              |   7
payroll/payment.py                     |   5
tests/test_payroll.py                  |   5
payroll/company.py                     |   4
Makefile                               |   4
--------------------------------------------------
```

## To run the tests:

There are unit tests and one functional (end-to-end) test. You can run them like this:

```
make unit (or make test)
make functional
make testall
make coverage
```
