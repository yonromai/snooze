# Snooze

[![Build Status](https://travis-ci.com/yonromai/snooze.svg?branch=master)](https://travis-ci.com/github/yonromai/snooze)
[![Code Coverage](https://codecov.io/gh/yonromai/snooze/branch/master/graph/badge.svg)](https://codecov.io/gh/yonromai/snooze)

---

Leave reminders in your code. Useful to set a timer on FIXMEs, TODOs & scheduled releases. 


## Example

If you leave a snooze in `./foo.py`:
```python
# snooze: 1900-01-01
lib.broken_logic = my_fixed_logic # FIXME: remove when lib==0.42 gets released
```

You can find the expired snoozes using the CLI:
```
$ snooze
Searching directory "." for snoozes
foo.py:1 - #        snooze: 1900-01-01
```
## Notes
* If matches are found, the CLI will return a non 0 exit code so it can be used in builds/precommit-hooks.
* Dates must be represented as [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

## TODO
* Publish to Pypi
* Add License headers
* add badges to README.md
