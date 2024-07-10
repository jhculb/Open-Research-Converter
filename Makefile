all: code_quality test security_test

code_quality: format_and_lint_ruff prerun_precommit

test: test_coverage

security_test: bandit

format_and_lint_ruff:
	poetry run ruff format
	poetry run ruff check --fix

lint_flake8:
	poetry run flake8 ./src

lint_pylint:
	poetry run pylint "./src/"

prerun_black:
	poetry run black ./src

prerun_precommit:
	pre-commit run --all

test_coverage:
	poetry run coverage run -m pytest ./tests

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
