import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == '1'
PRODUCTION = str(os.environ.get('PRODUCTION')) == '1'

INTERNAL_IPS = ['127.0.0.1', 'localhost',]

ALLOWED_HOSTS = ['englishstuff.online', 'www.englishstuff.online', '207.154.205.99', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # own apps
    'pages',
    'quiz',
    'socialmedia',
    'blog',

    # thid-party apps
    'markdownx',
    'django_htmx',
    'analytical',
    'captcha',
    'crispy_forms',
    # 'django_minify_html',
    # 'compressor',
    # 'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'taggit',
    'django_social_share',

]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



# https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    # 'django_minify_html.middleware.MinifyHtmlMiddleware',
]


ROOT_URLCONF = 'config.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.general',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

USE_SQLITE3_DB = str(os.environ.get('USE_SQLITE3_DB')) == '1'

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_TESTS_DB = os.environ.get('POSTGRES_TESTS_DB')


if USE_SQLITE3_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': POSTGRES_HOST,
            'PORT': POSTGRES_PORT,
            'TEST': {
             'NAME': 'test_db',
             },
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True



# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# analytics
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = 'G-5ZBMDVB7S4'

# seo

SITE_TITLE = 'English Stuff Online'
META_KEYWORDS = 'learn, English, learning, practice, quiz, advanced, prepositions, collocations, stuff, exam, cambridge, trinity'
META_DESCRIPTION = 'English Stuff Online. Learn and practice english with quizzes for free | Phrasal verbs, prepositions, collocations, common mistakes, ... '

# socialmedia app 
# Telegram

TELEGRAM_BOT_API_KEY = os.environ.get("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHANNEL_NAME = '@english_stuff_online'


# Linkedin
LINKEDIN_CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID") # not needed at the moment
LINKEDIN_CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET") # not needed at the moment
LINKEDIN_PROFILE_ID = os.environ.get("LINKEDIN_PROFILE_ID")
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")


LINKEDIN_ORGANIZATION_ID = os.environ.get("LINKEDIN_ORGANIZATION_ID")
LINKEDIN_ORGANIZATION_ACCESS_TOKEN = os.environ.get("LINKEDIN_ORGANIZATION_ACCESS_TOKEN")
LINKEDIN_ORGANIZATION_REFRESH_TOKEN = os.environ.get("LINKEDIN_ORGANIZATION_REFRESH_TOKEN")


# Twitter
TWITTER_USERNAME = 'EnglishstuffOn'

TWITTER_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.environ.get("TWITTER_CLIENT_SECRET")

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")

TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# Facebook
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID")
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET_KEY = os.environ.get("FACEBOOK_APP_SECRET_KEY")

# Instagram
INSTAGRAM_PAGE_ID = os.environ.get("INSTAGRAM_PAGE_ID")
INSTAGRAM_ACCESS_TOKEN =os.environ.get("INSTAGRAM_ACCESS_TOKEN")


# celery
from celery.schedules import crontab
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'django-db'

CELERY_BEAT_SCHEDULE = {
      'share_random_question': {
        'task': 'socialmedia.tasks.share_random_question_instance',
        'schedule': crontab(hour=12, minute=00),
        'options': {
            'expires': 0,
        },
    },
      'share_regular_social_post': {
        'task': 'socialmedia.tasks.share_regular_social_post',
        'schedule': crontab(hour=9, minute=30), # when more instances available: add crontab(hour='8,13', minute=00)
        'options': {
            'expires': 0,
        },
    },
}



# DeepL API
DEEPL_AUTH_KEY = os.environ.get('DEEPL_AUTH_KEY')


# Storage
USE_SPACES = os.environ.get('USE_SPACES') == '1'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_dev'),
]

if USE_SPACES:

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = 'spaces.ramiboutas.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', 'ACL': 'public-read'}
    # AWS_LOCATION = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com'

    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaRootStorage'
    STATICFILES_STORAGE = 'config.storage_backends.StaticRootStorage'

    AWS_STATIC_LOCATION = 'englishstuff-static'
    # STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_STATIC_LOCATION}/'
    STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    STATIC_ROOT = f'{AWS_STATIC_LOCATION}/'

    AWS_MEDIA_LOCATION = 'englishstuff-media'
    # MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com/{AWS_MEDIA_LOCATION}/' # it worked
    # MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_LOCATION}/'
    MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
    MEDIA_ROOT = f'{AWS_MEDIA_LOCATION}/'



else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = "access-control-allow-origin"



if PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000 #31536000 # usual: 31536000 (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    PREPEND_WWW = True

    # caching
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379',
        }
    }
