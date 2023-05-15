FROM mcr.microsoft.com/devcontainers/python:3

RUN python -m pip install --upgrade pip \
    && python -m pip install 'flit>=3.8.0'

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - \
	&& apt install nodejs

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN touch README.md \
    && mkdir -p src/python_package \
    && python -m flit install --only-deps --deps develop \
    && rm -r pyproject.toml README.md src
