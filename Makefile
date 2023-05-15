all: code_quality lint test

code_quality: prerun_black prerun_precommit

lint: lint_flake8 lint_pylint

test: test_coverage

lint_flake8:
	flake8 .

lint_pylint:
	pylint "src/"

prerun_black:
	black .

prerun_precommit:
	pre-commit run --all

test_coverage:
	python -m coverage run -m pytest ./tests
