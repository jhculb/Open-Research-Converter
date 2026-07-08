ARG PYTHON_VERSION=3.11.10

FROM python:${PYTHON_VERSION} AS project-base

ARG POETRY_VERSION=1.8.3

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

FROM project-base AS project-install

WORKDIR /app/

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry install --without dev --no-root

FROM project-install AS project-runner

# ENV GUNICORN_WORKER_COUNT=9 GUNICORN_WORKER_TIMEOUT=30

ARG APP_PORT=8001

COPY src/orc/backend /app/src/orc/backend

RUN poetry install --without dev

WORKDIR /app/src/orc/backend/orc_backend

EXPOSE ${APP_PORT}

# Use sh -c so GUNICORN_NUM_WORKERS / GUNICORN_LOG_LEVEL from the env file are
# honoured (the old exec-array form hardcoded 9 workers and ignored the env,
# which caused OOM kills on memory-limited hosts). `exec` keeps gunicorn as PID 1
# so it still receives SIGTERM for graceful shutdown.
ENTRYPOINT ["sh", "-c", "exec poetry run gunicorn app:app --worker-class uvicorn.workers.UvicornWorker -w ${GUNICORN_NUM_WORKERS:-9} -b 0.0.0.0:8001 --access-logfile /app/logs/gunicorn_access.log --error-logfile /app/logs/gunicorn_error.log --log-level ${GUNICORN_LOG_LEVEL:-info} --timeout ${GUNICORN_TIMEOUT:-60}"]
