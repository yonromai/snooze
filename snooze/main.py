import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from dateutil.parser import parse

from snooze.parser import DEFAULT_WOKERS, SnoozeParser


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Leave reminders in your code. Useful to set a timer on FIXMEs, TODOs & scheduled releases."
    )
    parser.add_argument(
        "directory",
        default=".",
        type=str,
        nargs="?",
        help="Path of the directory to search for snoozes",
    )
    parser.add_argument(
        "--time",
        default=None,
        type=str,
        help="Time (ISO 8601) used to tell whether snoozes are triggered (default: now)",
    )
    parser.add_argument(
        "--threads",
        default=DEFAULT_WOKERS,
        type=int,
        help=f"Number of threads used to parse files (default: {DEFAULT_WOKERS})",
    )
    assert len(argv) >= 1, "args should start with the program executable"
    return parser.parse_args(args=argv[1:])


def main(argv: List[str] = sys.argv) -> None:
    args = parse_args(argv)
    directory = Path(args.directory)
    time = parse(args.time) if args.time else datetime.utcnow()
    processes = args.threads
    if not directory.exists():
        print(f"ERROR: Could not find directory: {directory}")
        sys.exit(os.EX_USAGE)

    print(f'Searching directory "{directory}" for snoozes')
    found_matches = False

    for match in SnoozeParser.search_all_files(
        root_dir=directory, now=time, processes=processes
    ):
        found_matches = True
        print(match)

    if found_matches:
        sys.exit(os.EX_DATAERR)
    print("No triggered snooze found.")
    sys.exit(os.EX_OK)
