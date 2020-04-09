import sys

from setuptools import setup

assert sys.version_info >= (3, 5, 0), "Snooze requires Python 3.5+"


setup(
    use_scm_version={
        "write_to": "snooze/__version__.py",
        "write_to_template": 'version = "{version}"\n',
    },
    # Keep this in sync with Pipfile / packages
    install_requires=["dataclasses", "python-dateutil"],
    # Keep this in sync with Pipfile / dev-packages
    extras_require={
        "dev": ["black==19.10b0", "flake8", "flake8-mypy", "isort", "mypy", "pytest"],
    },
    setup_requires=["setuptools-scm", "setuptools>=40.0"],
)
