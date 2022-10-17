FROM python:3.10

EXPOSE 8000

WORKDIR /app

ENV PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

ADD poetry.lock  pyproject.toml ./

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    curl \
    gcc \
    libpq-dev \
    netcat \
 && curl -sSL https://install.python-poetry.org | python - \
 && poetry install \
 && apt-get autoremove -qqy gcc

ADD . .
