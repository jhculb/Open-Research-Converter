all: code_quality lint_and_fix test security

all_no_fix: code_quality lint test security

code_quality: prerun_ruff_formatter prerun_precommit

lint:
	poetry run ruff check ./src

lint_and_fix:
	poetry run ruff check --select I --fix ./src

test: test_coverage

security: bandit

prerun_ruff_formatter:
	poetry run ruff format ./src

prerun_precommit:
	pre-commit run --all

test_coverage:
	poetry run coverage run -m pytest ./tests

test_pytest:
	poetry run pytest ./tests

bandit:
	poetry run bandit -c pyproject.toml -r ./src/

install_locally:
	python -m pip install --upgrade pip
	pip install poetry==1.5.1
	poetry install --only dev --no-root
	pip install pre-commit==3.3.2
	pre-commit install-hooks

test_badges:
	mkdir badges
	python generate_badges.py
