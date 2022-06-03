import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT = "testproject"
PROJECT_VERBOSE = "Test Project"

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "localhost")
HOSTNAME = os.environ.get("ALLOWED_HOST", f"{PROJECT}.{DOMAIN_NAME}")
ALLOWED_HOSTS = [HOSTNAME, f"{HOSTNAME}:8000"]
ALLOWED_HOSTS += [f"www.{host}" for host in ALLOWED_HOSTS]

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

INSTALLED_APPS = [
    PROJECT,
    "ndh",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "bootstrap4",
    "mergics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = f"{PROJECT}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = f"{PROJECT}.wsgi.application"

DB = os.environ.get("DB", "db.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / DB,
    }
}
if DB == "postgres":
    DATABASES["default"].update(
        ENGINE="django.db.backends.postgresql",
        NAME=os.environ.get("POSTGRES_DB", DB),
        USER=os.environ.get("POSTGRES_USER", DB),
        HOST=os.environ.get("POSTGRES_HOST", DB),
        PASSWORD=os.environ["POSTGRES_PASSWORD"],
    )

_APV = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{_APV}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{_APV}.MinimumLengthValidator",
    },
    {
        "NAME": f"{_APV}.CommonPasswordValidator",
    },
    {
        "NAME": f"{_APV}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "fr-FR")
TIME_ZONE = os.environ.get("TIME_ZONE", "Europe/Paris")
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = int(os.environ.get("SITE_ID", 1))

MEDIA_ROOT = f"/srv/{PROJECT}/media/"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = f"/srv/{PROJECT}/static/"
LOGIN_REDIRECT_URL = "/"

EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST = "mail.gandi.net"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", f"majo@{HOSTNAME}")
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = f"{PROJECT_VERBOSE} <{EMAIL_HOST_USER}>"
SERVER_EMAIL = f"Server {DEFAULT_FROM_EMAIL}"
REPLY_TO = f"webmaster@{HOSTNAME}"
ADMINS = [(f"{PROJECT_VERBOSE} Webmasters", "webmaster@{HOSTNAME}")]

if os.environ.get("MEMCACHED", "False").lower() == "true":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "memcached:11211",
        }
    }

AUTHENTICATION_BACKENDS = ["yeouia.backends.YummyEmailOrUsernameInsensitiveAuth"]
