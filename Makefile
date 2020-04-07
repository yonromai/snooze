init:
	pip install -r requirements.txt

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
