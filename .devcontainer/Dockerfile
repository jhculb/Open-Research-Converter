FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip \
	&& curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - --version 1.2.0 \
	&& poetry completions bash >> ~/.bash_completion

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN poetry self update
