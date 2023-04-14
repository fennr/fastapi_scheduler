FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# POETRY_VIRTUALENVS_IN_PROJECT is required to ensure in-projects venvs mounted from the host in dev
# don't get prioritised by `poetry run`
ENV POETRY_VERSION=1.3.2 \
  POETRY_HOME="/opt/poetry/home" \
  POETRY_CACHE_DIR="/opt/poetry/cache" \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=false

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install --no-install-recommends -y curl \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python

WORKDIR /ds

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
  poetry lock && \
  poetry install --no-root --without dev

COPY main.py ./
COPY ./app ./app

EXPOSE 8000


CMD [ "poetry", "run", "python", "main.py" ]
