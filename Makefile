all: code_quality lint test security_test

code_quality: format_ruff prerun_precommit

lint: lint_ruff

test: test_coverage

security_test: bandit

lint_ruff:
	poetry run ruff check

format_ruff:
	poetry run ruff format

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

react_frontend:
#   install node.js and npm (for me the working versions are node=16.17.1 and npm=8.15.0)
    go to directory: cd /src/orc/frontend/orc-demo
    npm install     # to install required modules/packages before running
    npm start       # to run a project
    npm run build   # to create a production build

