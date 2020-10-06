FROM python:slim

EXPOSE 8000

WORKDIR /app

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=off PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_IN_PROJECT=true PATH=/root/.poetry/bin:/app/.venv/bin:$PATH

ADD poetry.lock  pyproject.toml ./

RUN apt-get update -qqy \
 && apt-get install -qqy \
    curl \
    gcc \
    libpq-dev \
    netcat \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
 && poetry install --no-root \
 && apt-get autoremove -qqy gcc \
 && rm -rf /var/lib/apt/lists/* /root/.poetry

ADD . .
