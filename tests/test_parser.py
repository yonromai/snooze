# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from pathlib import Path

from _pytest.logging import LogCaptureFixture

from snooze.parser import SnoozeMatch, SnoozeParser


def test__file_ext() -> None:
    assert SnoozeParser._file_ext(Path("foo/bar.py")) == "py"
    assert SnoozeParser._file_ext(Path("foo")) is None


def test__mk_snooze_regex() -> None:
    regex = SnoozeParser._mk_snooze_regex("py")
    assert regex.match("  # snooze: 1900-01-01")
    assert regex.match("print('foo') # snooze: 1900-01-01")
    assert not regex.match("dummy")
    assert not regex.match("# dummy")
    assert not regex.match("  snooze: 1900-01-01")


def test__matches_in_file(test_resources: Path) -> None:
    hw_py = test_resources / "hello_world.py"
    matches = list(
        SnoozeParser._matches_in_file(
            hw_py, now=datetime(year=1899, month=12, day=31), root=test_resources
        )
    )
    assert matches == [
        SnoozeMatch(
            path=Path("hello_world.py"),
            line='print("Hello, world!")  # snooze: 1900-01-01',
            line_nb=1,
            time=datetime(1900, 1, 1, 0, 0),
        )
    ]
    matches = list(
        SnoozeParser._matches_in_file(
            hw_py, now=datetime(year=1900, month=1, day=1), root=test_resources
        )
    )
    assert matches == [
        SnoozeMatch(
            path=Path("hello_world.py"),
            line='print("Hello, world!")  # snooze: 1900-01-01',
            line_nb=1,
            time=datetime(1900, 1, 1, 0, 0),
        )
    ]
    matches = list(
        SnoozeParser._matches_in_file(
            hw_py, now=datetime(year=1900, month=1, day=2), root=test_resources
        )
    )
    assert len(matches) == 0


def test__try_parse_time(caplog: LogCaptureFixture) -> None:
    regex = SnoozeParser._mk_snooze_regex("py")
    time = SnoozeParser._try_parse_time(regex=regex, line="", path=Path("/dummy"), i=42)
    assert time is None
    time = SnoozeParser._try_parse_time(
        regex=regex, line="foo # snooze: 1900-01-01", path=Path("/dummy"), i=42
    )
    assert time == datetime(1900, 1, 1)
    # with pytest.warns(Warning, match=r"Could not parse time \"1900-33-33\""):
    with caplog.at_level(logging.WARNING):
        time = SnoozeParser._try_parse_time(
            regex=regex, line="foo # snooze: 1900-33-33", path=Path("/dummy.py"), i=42
        )
        assert time is None
        assert caplog.text.strip().startswith("WARNING  root:parser.py:")
        caplog.text.strip().endswith(
            'Could not parse time "1900-33-33" in /dummy.py:42'
        )


def test_search_all_files(test_resources: Path) -> None:
    matches = list(
        SnoozeParser.search_all_files(
            test_resources, now=datetime(year=1900, month=1, day=1)
        )
    )
    assert sorted(matches) == sorted(
        [
            SnoozeMatch(
                path=Path("hello_world.py"),
                line='print("Hello, world!")  # snooze: 1900-01-01',
                line_nb=1,
                time=datetime(1900, 1, 1, 0, 0),
            ),
            SnoozeMatch(
                path=Path("hello_world.c"),
                line='   printf("Hello, World!"); // snooze: 1900-01-01',
                line_nb=3,
                time=datetime(1900, 1, 1, 0, 0),
            ),
            SnoozeMatch(
                path=Path("hello_world.js"),
                line='console.log("Hello, World!");  // snooze: 1900-01-01',
                line_nb=1,
                time=datetime(1900, 1, 1, 0, 0),
            ),
            SnoozeMatch(
                path=Path("hello_world.cpp"),
                line='    std::cout << "Hello World!"; // snooze: 1900-01-01',
                line_nb=3,
                time=datetime(1900, 1, 1, 0, 0),
            ),
            SnoozeMatch(
                path=Path("hello_world.java"),
                line='        System.out.println("Hello, World!"); // snooze: 1900-01-01',
                line_nb=3,
                time=datetime(1900, 1, 1, 0, 0),
            ),
        ]
    )


def test_sort() -> None:
    matches = [
        SnoozeMatch(
            path=Path("/path/2"), line="line1", line_nb=1, time=datetime(1900, 1, 1)
        ),
        SnoozeMatch(
            path=Path("/path/1"), line="line2", line_nb=2, time=datetime(1900, 1, 1)
        ),
        SnoozeMatch(
            path=Path("/path/1"), line="line1", line_nb=1, time=datetime(1900, 1, 1)
        ),
    ]
    sorted_matches = sorted(matches)
    assert [(m.path, m.line) for m in sorted_matches] == [
        (Path("/path/1"), "line1"),
        (Path("/path/1"), "line2"),
        (Path("/path/2"), "line1"),
    ]
