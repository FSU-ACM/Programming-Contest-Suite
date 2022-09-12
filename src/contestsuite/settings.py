"""
Django settings for contestsuite project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ

SECRET_KEY = os.environ.get('SECRET_KEY', '86@j2=z!=&1r_hoqboog1#*mb$jx=9mf0uw#hrs@lw&7m34sqz')

# SECURITY WARNING: don't run with debug turned on in production!
# False if not in os.environ

if os.environ.get('DEBUG'):
    DEBUG = os.environ.get('DEBUG') == 'True'
else:
    DEBUG = False


if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '[::1]']
else:
    if os.environ.get('ALLOWED_HOSTS'):
        ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
    else:
        ALLOWED_HOSTS = []
        
    
# Debug Toolbar Access 

if DEBUG:
    INTERNAL_IPS = [
        'localhost',
        '0.0.0.0',
        '127.0.0.1',
    ]


# Application definition

INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # User defined
    'announcements.apps.AnnouncementsConfig',
    'checkin.apps.CheckinConfig',
    'contestadmin.apps.ContestAdminConfig',
    'core.apps.CoreConfig',
    'lfg.apps.LfgConfig',
    'manager.apps.ManagerConfig',
    'register.apps.RegisterConfig',
    # 3rd party packages
    'django_celery_beat',
    'import_export',
]

# Add debug_toolber only if site is in debug mode
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add debug_toolber middleware only if site is in debug mode
if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


ROOT_URLCONF = 'contestsuite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'contestsuite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
# read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '3306'),
        'NAME': os.environ.get('SQL_DATABASE', 'contestsuite'),
        'USER': os.environ.get('SQL_USER', 'contestadmin1!'),
        'PASSWORD': os.environ.get('SQL_PASSWORD','seminoles1!'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'TIME_ZONE': 'America/New_York',
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Celery
# https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#configuration
 
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'amqp://127.0.0.1:5672')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://127.0.0.1:6379/1')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'America/New_York')
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULE = {
    'cleanup-lfg-rosters': { 
         'task': 'lfg.tasks.cleanup_lfg_rosters', 
         'schedule': 600.0,
        },
    'scrape-discord-members': { 
         'task': 'lfg.tasks.scrape_discord_members', 
         'schedule': 1800.0,
        },
    'verify-lfg-profiles': { 
        'task': 'lfg.tasks.verify_lfg_profiles', 
        'schedule': 600.0,
    },          
}

# Cache
# https://docs.djangoproject.com/en/2.2/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('CACHE_LOCATION', 'redis://127.0.0.1:6379/0'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

if DEBUG:
    CACHE_TIMEOUT = 0
else:
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', 300))


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', 'America/New_York')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'


# Uploaded files (TSV)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Redirect to home URL after login (Default redirects to /accounts/profile/)

LOGIN_REDIRECT_URL = '/manage/'


# Sessions
# https://docs.djangoproject.com/en/3.2/topics/http/sessions/

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

if not DEBUG:
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Messages
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Email
# https://docs.djangoproject.com/en/3.1/topics/email/

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')  
    EMAIL_HOST = os.environ.get('EMAIL_HOST', None)
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_HOST_USER = os.environ.get('EMAIL_USER', None)
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', None)
    
    if os.environ.get('EMAIL_USE_SSL'):
        EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL') == 'True'
    else:
        EMAIL_USE_SSL = False
    
    if os.environ.get('EMAIL_USE_TLS'):
        EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
    else:
        EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'ACM at FSU Programming Contest<acm@cs.fsu.edu>')


# Discord
# https://discordpy.readthedocs.io/en/stable/

ANNOUNCEMENT_WEBHOOK_URL = os.environ.get('ANNOUNCEMENT_WEBHOOK_URL', None)
BOT_CHANNEL_WEBHOOK_URL = os.environ.get('BOT_CHANNEL_WEBHOOK_URL', None)
GUILD_ID = int(os.environ.get('GUILD_ID', 0))
SCRAPE_BOT_TOKEN = os.environ.get('SCRAPE_BOT_TOKEN', None)


# DOMjudge Status Button

DOMJUDGE_URL = os.environ.get('DOMJUDGE_URL', 'https://domjudge.cs.fsu.edu')


# Hashid Fields
# https://pypi.org/project/django-hashid-field/

HASHID_FIELD_SALT = os.environ.get(
    'HASHID_FIELD_SALT', '0s97rx*t4%68jell&lw3^)97o*kr*+*2o^(76q)ix+ilc!4ax#')
