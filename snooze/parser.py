# -*- coding: utf-8 -*-
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache, partial
from multiprocessing import cpu_count, pool
from pathlib import Path
from typing import Iterable, Optional, Pattern

from dateutil.parser import parse

from snooze.comments import comments_by_ext

DEFAULT_WOKERS = cpu_count()


@dataclass
class SnoozeMatch:
    path: Path
    line: str
    line_nb: int
    time: datetime

    def __str__(self):
        return f"{self.path}:{self.line_nb} - {self.line}"

    def __lt__(self, other: "SnoozeMatch") -> bool:
        if self.path == other.path:
            return self.line_nb < other.line_nb
        return self.path < other.path


class SnoozeParser:
    @staticmethod
    def _file_ext(p: Path) -> Optional[str]:
        if p.is_dir() or "." not in p.name:
            return None
        return p.name.rsplit(".", 1)[-1]

    @classmethod
    def _list_files(cls, root_dir: Path) -> Iterable[Path]:
        for p in root_dir.glob("**/*"):
            if cls._file_ext(p) in comments_by_ext:
                yield p

    @staticmethod
    @lru_cache(maxsize=8)
    def _mk_snooze_regex(file_ext: str) -> Pattern[str]:
        comment = comments_by_ext[file_ext]
        iso_8601_charset = r"[0-9\-:TWZ]+"
        return re.compile(rf"^.*{comment}\s?snooze:\s?({iso_8601_charset})")

    @classmethod
    def _matches_in_file(
        cls, path: Path, now: datetime, root: Path
    ) -> Iterable[SnoozeMatch]:
        regex = cls._mk_snooze_regex(cls._file_ext(path))
        for i, line in enumerate(path.read_text().splitlines()):
            match = regex.match(line)
            if match:
                timestr = match.groups()[0]
                try:
                    time = parse(timestr)
                    if time >= now:
                        yield SnoozeMatch(path.relative_to(root), line, i, time)
                except ValueError:
                    logging.warning(
                        f'Could not parse time "{timestr}" in {path.as_posix()}:{i}'
                    )

    @classmethod
    def search_all_files(
        cls,
        root_dir: Path,
        now: datetime = datetime.now(),
        processes: int = DEFAULT_WOKERS,
    ) -> Iterable[SnoozeMatch]:
        fn = partial(cls._matches_in_file, now=now, root=root_dir)
        with pool.ThreadPool(processes) as p:
            for matches in p.imap(fn, cls._list_files(root_dir)):
                yield from sorted(matches)
