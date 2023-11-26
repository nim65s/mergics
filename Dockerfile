FROM python:3.12

EXPOSE 8000

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    --mount=type=cache,sharing=locked,target=/root/.cache \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qqy --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-openbsd \
 && python -m pip install -U pip \
 && python -m pip install -U pipx \
 && python -m pipx install poetry

ADD pyproject.toml poetry.lock ./
RUN --mount=type=cache,sharing=locked,target=/root/.cache \
    poetry install --with prod --no-root --no-interaction --no-ansi

ADD . .
