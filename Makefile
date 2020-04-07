init:
	pip install pipenv --upgrade
	pipenv install --dev

check:
	black --check .
	flake8
	isort --check-only
	mypy .

autofix:
	isort
	black .

test:
	pytest
