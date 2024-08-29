all: code_quality lint_and_fix test security

all_no_fix: code_quality lint test security

code_quality: prerun_ruff_formatter prerun_precommit

lint:
	poetry run ruff check ./src

lint_and_fix:
	poetry run ruff check --select I --fix ./src

test: test_coverage

test_v: test_coverage_v

test_vv: test_coverage_vv

security: bandit

prerun_ruff_formatter:
	poetry run ruff format ./src

prerun_precommit:
	pre-commit run --all

test_coverage:
	poetry run coverage run -m pytest --capture=tee-sys ./tests

test_coverage_v:
	poetry run coverage run -m pytest -v --capture=tee-sys ./tests

test_coverage_vv:
	poetry run coverage run -m pytest -vv --capture=tee-sys ./tests

test_pytest:
	poetry run pytest --capture=tee-sys ./tests

bandit:
	poetry run bandit -c pyproject.toml -r ./src/

install_locally:
	python -m pip install --upgrade pip
	pip install poetry==1.8.3
	poetry install --with dev --no-root
	pip install pre-commit==3.3.2
	pre-commit install-hooks

install_pyright:
	python -m pip install --upgrade pip
	pip install poetry==1.8.3
	poetry config --local virtualenvs.in-project true
	poetry install

run:
	docker-compose down && docker-compose up --build -d

redeploy:
	git pull && docker-compose down && docker-compose up --build -d

view_container_logs_backend:
	docker logs --tail 50 --follow --timestamps orc-backend

view_container_logs_frontend:
	docker logs --tail 50 --follow --timestamps orc-frontend

view_container_logs_reverse_proxy:
	docker logs --tail 50 --follow --timestamps reverse-proxy

view_running_containers:
	docker ps

test_badges:
	mkdir badges
	python generate_badges.py

# react_frontend:
# #   install node.js and npm (for me the working versions are node=16.17.1 and npm=8.15.0)
#     go to directory: cd /src/orc/frontend/orc-demo
#     npm install     # to install required modules/packages before running
#     npm start       # to run a project
#     npm run build   # to create a production build
