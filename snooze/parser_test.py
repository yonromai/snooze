# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

import pytest

from snooze.parser import SnoozeMatch, SnoozeParser


@pytest.fixture
def test_resources() -> Path:
    return Path(__file__).parent / "test_resources"


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
