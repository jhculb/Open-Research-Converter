# Cross-platform detection
ifeq ($(OS),Windows_NT)
    COPY = copy
    PATHSEP = \\
    # compile_paper is not supported on Windows (requires id -u, id -g)
    COMPILE_PAPER_SUPPORTED = false
else
    COPY = cp
    PATHSEP = /
    COMPILE_PAPER_SUPPORTED = true
endif

all: code_quality lint_and_fix test security

all_no_fix: code_quality lint test security

code_quality: prerun_ruff_formatter prerun_precommit

lint:
	poetry run ruff check ./src

lint_and_fix:
	poetry run ruff check --select I --fix ./src

test: test_coverage

test_full:
	test_coverage test_coverage_integration test_javascript

test_v: test_coverage_v

test_vv: test_coverage_vv

test_javascript:
	cd ./src/orc/frontend/orc-demo && npm test

security: bandit

prerun_ruff_formatter:
	poetry run ruff format ./src

prerun_precommit:
	pre-commit run --all

test_coverage:
	poetry run coverage run -m pytest --capture=tee-sys ./tests

test_coverage_integration:
	poetry run coverage run -m pytest -m integration --capture=tee-sys ./tests

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
	docker compose down && docker compose up --build -d

redeploy:
	git pull && docker compose down && docker compose up --build -d

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

certificates_dry_run:
	docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d orc-demo.gesis.org

certificates_renew:
	docker compose run --rm certbot renew --webroot --webroot-path /var/www/certbot/ -n

certificates_create_and_load:
	docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d orc-demo.gesis.org

set_envs:
	$(COPY) .env.template .env
	$(COPY) src$(PATHSEP)env_templates$(PATHSEP)backend.env.template src$(PATHSEP)env$(PATHSEP)backend.env
	$(COPY) src$(PATHSEP)env_templates$(PATHSEP)frontend.env.template src$(PATHSEP)env$(PATHSEP)frontend.env
	$(COPY) src$(PATHSEP)env_templates$(PATHSEP)nginx.env.template src$(PATHSEP)env$(PATHSEP)nginx.env
	$(COPY) src$(PATHSEP)env_templates$(PATHSEP)js.env.template src$(PATHSEP)env$(PATHSEP)js.env

compile_paper:
ifeq ($(COMPILE_PAPER_SUPPORTED),true)
	docker run --rm --volume $(CURDIR)/paper:/data --user $(shell id -u):$(shell id -g) --env JOURNAL=joss openjournals/inara
else
	@echo "compile_paper is not supported on Windows (requires Unix id command)"
endif
