FROM python:latest AS project-base

ARG POETRY_VERSION=1.5.1

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

FROM project-base AS project-install

WORKDIR /app/

COPY pyproject.toml poetry.lock README.md /app/
COPY src/orc/backend /app/src/orc/backend

RUN poetry install --without dev

FROM project-install AS project-runner

EXPOSE 8002
WORKDIR /app/src/orc/backend/orc_backend

ENTRYPOINT [ "poetry", "run gunicorn", "app:app", "-b", "0.0.0.0:8002" ]
