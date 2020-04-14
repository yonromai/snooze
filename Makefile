all: autofix check test

init:
	pip install pipenv --upgrade
	pipenv install --dev

check:
	black --check .
	flake8
	isort --check-only
	mypy .

autofix:
	isort --apply
	black .

test:
	pytest --cov=snooze --cov-report=term --cov-report=html
