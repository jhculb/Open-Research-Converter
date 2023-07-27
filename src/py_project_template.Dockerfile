FROM python:latest AS project-base

ARG POETRY_VERSION=1.5.1

RUN python -m pip install --upgrade pip \
	&& pip install "poetry==$POETRY_VERSION"

FROM project-base AS project-runner

WORKDIR /src/

COPY ./src/py_project_template/ ./

RUN poetry install --without dev

CMD ["python", "py_project_template/hello_world.py"]
