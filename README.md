# Snooze

Leave reminders in your code. Useful to set a timer on FIXMEs, TODOs & scheduled releases. 

## Example

If you leave a snooze in `./foo.py`:
```python
# snooze: 1900-01-01
lib.broken_logic = my_fixed_logic # FIXME: remove when lib==0.42 gets released
```

You can find the expired snoozes using the CLI:
```
$ snooze .
> 1 triggered snooze found:
foo.py
1:# snooze: 1900-01-01
2-lib.broken_logic = my_fixed_logic # FIXME: remove when lib==0.42 gets released
```
## Notes
* If matches are found, the CLI will return a non 0 exit code so it can be used in builds/precommit-hooks.
* Dates must be represented as [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

## TODO
* Add bin entrypoint
* Publish to Pypi
* Display codecov.io reports
* Fix `python3.7/site-packages is in the MYPYPATH. Please remove it.`
* Add License headers
* Moar test coverage
* add badges to README.md
