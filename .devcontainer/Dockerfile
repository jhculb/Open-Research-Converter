FROM mcr.microsoft.com/devcontainers/python:3 AS base

ENV NODE_VERSION=18.x
RUN curl -fsSL "https://deb.nodesource.com/setup_$NODE_VERSION" | bash - \
	&& apt-get install -y nodejs

FROM base AS devcontainer_final

ENV	PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_DEFAULT_TIMEOUT=100 \
	POETRY_VERSION=1.5.1

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only dev --no-root
