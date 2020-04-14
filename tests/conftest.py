from pathlib import Path

import pytest


@pytest.fixture
def test_resources() -> Path:
    return Path(__file__).parent / "test_resources"
