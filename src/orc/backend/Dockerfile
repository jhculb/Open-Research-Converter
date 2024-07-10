FROM python:latest AS project-base

ARG POETRY_VERSION=1.5.1

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

FROM project-base AS project-runner
EXPOSE 80/tcp
EXPOSE 443/tcp
EXPOSE 8003/tcp

WORKDIR /src/

COPY ./src/orc/backend/ ./

RUN poetry install --without dev

ENTRYPOINT [ "gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:8003" ]
