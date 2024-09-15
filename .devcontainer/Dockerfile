FROM mcr.microsoft.com/devcontainers/python:3 AS base

ARG NODE_VERSION=20.x
RUN curl -fsSL "https://deb.nodesource.com/setup_$NODE_VERSION" | bash - \
	&& apt-get install -y nodejs \
	&& apt-get clean

FROM base AS devcontainer-final

ARG POETRY_VERSION=1.8.3
ENV	PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_DEFAULT_TIMEOUT=100

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry install --only dev --no-root
