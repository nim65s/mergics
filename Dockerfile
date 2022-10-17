FROM python:3.10

EXPOSE 8000

WORKDIR /app

ENV PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    --mount=type=cache,sharing=locked,target=/root/.cache \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    curl \
    gcc \
    libpq-dev \
    netcat \
 && python -m pip install -U pip \
 && curl -sSL https://install.python-poetry.org | python - \
 && python -m pip install \
    gunicorn \
    psycopg2 \
 && apt-get autoremove -qqy gcc

ADD pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root --no-interaction --no-ansi

ADD . .
