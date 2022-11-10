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
try:
    command = sys.argv[1]
except IndexError:  # pragma: no cover
    command = "help"

if command != "test":  # pragma: no cover
    dotenv.load_dotenv(dotenv_path=BASE_DIR / ".env")


# The name of the class to use for starting the test suite.

TEST_RUNNER = "config.test.TestRunner"


# Production
PRODUCTION = os.environ.get("PRODUCTION", "") == "1"

# Use Postgres (otherwise Sqlite)
USE_POSTGRES = os.environ.get("USE_POSTGRES", "") == "1"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "some-tests-need-a-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get("DEBUG")) == "1"
PRODUCTION = str(os.environ.get("PRODUCTION")) == "1"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

ALLOWED_HOSTS = [
    "englishstuff.online",
    "www.englishstuff.online",
    "207.154.205.99",
    "localhost",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    # My apps
    "pages.apps.PagesConfig",
    "quiz.apps.QuizConfig",
    "socialmedia.apps.socialmediaConfig",
    "blog.apps.BlogConfig",
    "users.apps.UsersConfig",
    # Thid-party apps
    "markdownx",  # cloned
    "django_htmx",
    "analytical",
    "captcha",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_minify_html",
    "django_celery_beat",
    "django_celery_results",
    "taggit",
    "django_social_share",
    "newsfeed",
    "nested_inline",
    "corsheaders",
    # Django contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    # 'django.contrib.sites',
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
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
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

if USE_POSTGRES:
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
else:
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

# seo

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


# celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/4"
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/4"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True


# DeepL API
DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")


# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# newsfeed settings https://github.com/saadmk11/django-newsfeed
NEWSFEED_EMAIL_BATCH_WAIT = 5
NEWSFEED_EMAIL_BATCH_SIZE = 15
NEWSFEED_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
NEWSFEED_SITE_BASE_URL = (
    "https://englishstuff.online" if PRODUCTION else "http://localhost:8000"
)
NEWSFEED_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1


# Settings for smtp
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
if EMAIL_PORT is not None:
    EMAIL_PORT = int(EMAIL_PORT)


if PRODUCTION and not DEBUG:
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_USE_TLS = False
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Storage
USE_SPACES = os.environ.get("USE_SPACES") == "1"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),
]

if USE_SPACES:
    # Stuff that could be useful (comments):
    # AWS_LOCATION = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com'
    # MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com/{AWS_MEDIA_LOCATION}/' # it worked
    # MEDIA_URL = f'https://{AWS_s3_endpoint_url}/{AWS_MEDIA_LOCATION}/'
    # STATIC_URL = f'https://{AWS_s3_endpoint_url}/{AWS_STATIC_LOCATION}/'

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
    AWS_S3_CUSTOM_DOMAIN = "spaces.ramiboutas.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400", "ACL": "public-read"}

    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    DEFAULT_FILE_STORAGE = "config.storage_backends.MediaRootStorage"
    STATICFILES_STORAGE = "config.storage_backends.StaticRootStorage"

    AWS_STATIC_LOCATION = "englishstuff-static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
    STATIC_ROOT = f"{AWS_STATIC_LOCATION}/"

    AWS_MEDIA_LOCATION = "englishstuff-media"

    MEDIA_URL = f"{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
    MEDIA_ROOT = f"{AWS_MEDIA_LOCATION}/"

else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = "Access-Control-Allow-Origin"

# CORS_ALLOWED_ORIGINS = [
#     "https://spaces.ramiboutas.com",
# ]

if PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000  # 31536000 # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    PREPEND_WWW = True

    # caching
    CELERY_CACHE_BACKEND = "default"
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/4",
        }
    }
