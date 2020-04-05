# -*- coding: utf-8 -*-

from snooze.comments import comments_by_ext


def test_comments() -> None:
    assert "py" in comments_by_ext
