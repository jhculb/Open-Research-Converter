FROM python:3.11.10 AS project-base

ARG POETRY_VERSION=1.8.3

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

FROM project-base AS project-install

WORKDIR /app/

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry install --without dev --no-root

FROM project-install AS project-runner

COPY src/orc/backend /app/src/orc/backend

RUN poetry install --without dev

WORKDIR /app/src/orc/backend/orc_backend

EXPOSE 8001

ENTRYPOINT [ "poetry", "run", "gunicorn", "app:app", "--worker-class", "uvicorn.workers.UvicornWorker", "-w", "9", "-b", "0.0.0.0:8001", "--access-logfile", "/app/logs/gunicorn_access.log", "--error-logfile", "/app/logs/gunicorn_error.log", "--log-level", "debug", "--timeout", "0"]
