FROM python:3.9.19 AS project-base

ARG POETRY_VERSION=1.5.1

ENV GUNIORN_NUM_WORKERS=4

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

ENTRYPOINT [ "poetry", "run", "gunicorn", "app:app", "-b", "0.0.0.0:8001", "--access-logfile", "/app/logs/gunicorn_access.log", "--error-logfile", "/app/logs/gunicorn_error.log", "--log-level", "debug"]
