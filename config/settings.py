from __future__ import annotations

import os
import sys
from pathlib import Path

import django
import dotenv
from django.utils.encoding import force_str

# https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding
django.utils.encoding.force_text = force_str

# ImportError: cannot import name 'url' from 'django.conf.urls'
#  markdownx.urls
# from django.urls import re_path
# django.conf.urls.url = django.urls.re_path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load env vars from .env file if not testing
try:  # pragma: no cover
    command = sys.argv[1]
except IndexError:  # pragma: no cover
    command = "help"

if command != "test":  # pragma: no cover
    dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")

# The name of the class to use for starting the test suite.
TEST_RUNNER = "django_rich.test.RichRunner"

# Django secret key
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "some-tests-need-a-secret-key")

# Debug flag
DEBUG = os.environ.get("DEBUG", "") == "1"


# Use redis caching
USE_REDIS_CACHING = os.environ.get("USE_REDIS_CACHING", "") == "1"

# Use Postgres (otherwise SqLite)
USE_POSTGRES = os.environ.get("USE_POSTGRES", "") == "1"

# Use real email backend
USE_EMAIL_BACKEND = os.environ.get("USE_EMAIL_BACKEND", "") == "1"


# https for production
HTTPS = os.environ.get("HTTPS", "") == "1"


INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = [
    "englishstuff.online",
    "www.englishstuff.online",
    "hello.englishstuff.online",
    "207.154.205.99",
    "englishstuff.local",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    # My apps
    "core.apps.CoreConfig",
    "quiz.apps.QuizConfig",
    "socialmedia.apps.socialmediaConfig",
    "blog.apps.BlogConfig",
    "users.apps.UsersConfig",
    "affiliates.apps.AffiliatesConfig",
    # Thid-party apps
    "markdownx",  # cloned
    "django_htmx",
    "captcha",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_celery_beat",
    "django_celery_results",
    "taggit",
    "newsfeed",
    "nested_inline",
    "corsheaders",
    "request",
    "dbbackup",
    "django_minify_html",
    # Django contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    # "django.contrib.sites",
]


AUTH_USER_MODEL = "users.User"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# newsletter app
# https://forum.djangoproject.com/t/importerror-cannot-import-name-ugettext-lazy-from-django-utils-translation/10943

# from django.utils.translation import gettext_lazy, gettext
# django.utils.translation.ugettext_lazy = gettext_lazy
# django.utils.translation.ugettext = gettext


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "request.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_minify_html.middleware.MinifyHtmlMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.context_processors.general",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if USE_POSTGRES:  # pragma: no cover
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "")
    POSTGRES_TESTS_DB = os.environ.get("POSTGRES_TESTS_DB", "")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
            "TEST": {
                "NAME": "test_db",
            },
        }
    }
else:  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# 'postgres://${{ secrets.TESTING_POSTGRES_USER }}:${{ secrets.TESTING_POSTGRES_PASSWORD }}
# @localhost:5432/${{ secrets.TESTING_POSTGRES_DB }}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# analytics
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = "G-5ZBMDVB7S4"


# django-request
REQUEST_BASE_URL = "https://www.englishstuff.online"

REQUEST_IGNORE_PATHS = (
    r"^admin.*",
    "/robots.txt",
    "/favicon.ico",
)

REQUEST_TRAFFIC_MODULES = ("request.traffic.UniqueVisitor",)

# deny ips
NGIX_DENY_CONFIGURATION_FILE = "/etc/nginx/conf.d/deny.conf"

DENY_IPS_WITH_PATHS = [
    ".php",
    ".env",
    "wlwmanifest.xml",
    "config.json",
    ".production",
    ".local",
    ".remote",
]


# site info
SITE_TITLE = "English Stuff Online"
META_KEYWORDS = "learn, English, learning, practice, quiz, advanced, \
    prepositions, collocations, stuff, exam, cambridge, trinity"
META_DESCRIPTION = "English Stuff Online. \
    Learn and practice english with quizzes for free | \
    Phrasal verbs, prepositions, collocations, common mistakes, ... "


# Telegram - socialmedia app
TELEGRAM_BOT_API_KEY = os.environ.get("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHANNEL_NAME = "@english_stuff_online"


# Linkedin - socialmedia app
LINKEDIN_CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
LINKEDIN_PROFILE_ID = os.environ.get("LINKEDIN_PROFILE_ID")
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORGANIZATION_ID = os.environ.get("LINKEDIN_ORGANIZATION_ID")
LINKEDIN_ORGANIZATION_ACCESS_TOKEN = os.environ.get(
    "LINKEDIN_ORGANIZATION_ACCESS_TOKEN"
)
LINKEDIN_ORGANIZATION_REFRESH_TOKEN = os.environ.get(
    "LINKEDIN_ORGANIZATION_REFRESH_TOKEN"
)


# Twitter - socialmedia app
TWITTER_USERNAME = "EnglishstuffOn"
TWITTER_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.environ.get("TWITTER_CLIENT_SECRET")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")


# Facebook - socialmedia app
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET_KEY = os.environ.get("FACEBOOK_APP_SECRET_KEY")


# Instagram - socialmedia app
INSTAGRAM_PAGE_ID = os.environ.get("INSTAGRAM_PAGE_ID")
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")


# DeepL API
DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")


# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Newsfeed settings https://github.com/saadmk11/django-newsfeed
NEWSFEED_EMAIL_BATCH_WAIT = 5
NEWSFEED_EMAIL_BATCH_SIZE = 15
NEWSFEED_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
NEWSFEED_SITE_BASE_URL = "https://englishstuff.online"
NEWSFEED_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1


# celery

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True

# caching


if USE_REDIS_CACHING:  # pragma: no cover
    REDIS_CACHING_LOCATION = os.environ.get("REDIS_CACHING_LOCATION", "")
    CELERY_CACHE_BACKEND = "default"
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_CACHING_LOCATION,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

# SMTP Email
if USE_EMAIL_BACKEND:  # pragma: no cover
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT_STR = os.environ.get("EMAIL_PORT")
    EMAIL_PORT = int(EMAIL_PORT_STR) if EMAIL_PORT_STR is not None else 1234
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

else:  # pragma: no cover
    EMAIL_USE_TLS = False
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# geoip2

GEOIP_PATH = BASE_DIR / "geoip2dbs"


# Storage


# media storage (aws s3)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_MEDIA_LOCATION = "englishstuff-media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"

# static files (whitenoise)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STORAGES = {
    "default": {
        "BACKEND": "config.storage_backends.MediaRootStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Backups
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {
    "location": "/home/rami/do-server-backups/englishquiz/",
}


# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = "Access-Control-Allow-Origin"
# CORS_ALLOWED_ORIGINS = ["https://spaces.ramiboutas.com", ]

if HTTPS:  # pragma: no cover
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31_536_000  # 31536000 # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    PREPEND_WWW = False
