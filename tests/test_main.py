import os
from pathlib import Path
from typing import List

import pytest

from snooze import main


@pytest.fixture
def argv() -> List[str]:
    return ["foo/bar/bin/snooze"]


def test_main_no_args(argv: List[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv)
    assert e.value.code == os.EX_DATAERR


def test_main_help(argv: List[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + ["--help"])
    assert e.value.code == os.EX_OK


def test_main_dir_no_files(argv: List[str], tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + [tmp_path.as_posix()])
    assert e.value.code == os.EX_OK


def test_main_dir_matches(argv: List[str], test_resources: Path) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + [test_resources.as_posix()])
    assert e.value.code == os.EX_DATAERR


def test_main_invaid_dir(argv: List[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + ["/dir/does/not/exist"])
    assert e.value.code == os.EX_USAGE


def test_main_time(argv: List[str], test_resources: Path) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + [test_resources.as_posix(), "--time=1899-01-01"])
    assert e.value.code == os.EX_OK


def test_main_dir_threads(argv: List[str], tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as e:
        main.main(argv + [tmp_path.as_posix(), "--threads=1"])
    assert e.value.code == os.EX_OK
