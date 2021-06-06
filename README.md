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
< Git Repo Activity Report (Python files only) >
> Repo: payroll
--------------------------------------------------

* Repo inserts and deletes per day:

2021-05-30                             | 929
2021-06-01                             |  55
2021-06-02                             |  33

* Number of commits per day and author:

2021-05-30
- Bob Belderbos                        |  61
2021-06-01
- Bob Belderbos                        |   9
2021-06-02
- Bob Belderbos                        |  10

* Files that are most often found in commits:

payroll/payroll.py                     |  12
tests/conftest.py                      |  10
payroll/timesheet.py                   |   9
tests/test_objects.py                  |   9
payroll/employee.py                    |   8
payroll/payment.py                     |   5
tests/test_payroll.py                  |   5
payroll/company.py                     |   4
payroll/__init__.py                    |   4
tests/test_timesheet.py                |   4
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
