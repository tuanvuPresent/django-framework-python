import datetime
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config
from mongoengine import connect


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_config = config

SECRET_KEY = env_config('SECRET_KEY')
DEBUG = env_config("DEBUG", cast=bool)
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'apps.account',
    'apps.auth.jwt',
    'apps.common',
    'apps.e_learning',
    'apps.export_file',
    'apps.fcm_notify',
    'apps.import_file',
    'apps.my_phone_verify',
    'apps.paypal',
    'apps.sample',
    'apps.sample_els',
    'apps.sendmail',
    'apps.shops',
    'apps.totp',
    'apps.upfile',
    'apps.webhook',

    'rest_pyotp',
    'rest_framework.authtoken',
    'silk',
    'drf_yasg',
    'corsheaders',
    'django_crontab',
    'rest_framework',
    'django_celery_beat',
    'django_celery_results',
    'social_django',
    'fcm_django',
    'log_viewer',
    'graphene_django',
    'constance',
    'constance.backends.database',
    'django_elasticsearch_dsl_drf',
    'django_elasticsearch_dsl',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'apps.common.middleware.LogRequest',
]

# Cors
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8002',
]

ROOT_URLCONF = 'Example.urls'

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

WSGI_APPLICATION = 'Example.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if env_config('DATABASES_NAME', 'None').lower() == 'postgres':
    DATABASES = {
        "default": {
            "ENGINE": env_config("POSTGRES_ENGINE", "django.db.backends.sqlite3"),
            "NAME": env_config("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": env_config("POSTGRES_USER", "admin"),
            "PASSWORD": env_config("POSTGRES_PASSWORD", "admin"),
            "HOST": env_config("POSTGRES_HOST", "localhost"),
            "PORT": env_config("POSTGRES_PORT", "5432"),
        }
    }
elif env_config('DATABASES_NAME', 'None').lower() == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': env_config("MY_SQL_ENGINE", "django.db.backends.sqlite3"),
            'NAME': env_config("MYSQL_DATABASE", "db"),
            'USER': env_config("MYSQL_USER", "admin"),
            'PASSWORD': env_config("MYSQL_PASSWORD", "admin"),
            'HOST': env_config("MY_SQL_HOST", "127.0.0.1"),
            'PORT': env_config("MYSQL_PORT", "3306"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = env_config('LANGUAGE_CODE')

TIME_ZONE = env_config('TIME_ZONE')

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

TEMP_URL = '/temp/'
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
        'apps.common.custom_exception_handler.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'apps.common.custom_authentication.ExpiringTokenAuthentication'
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '12/min',
        'shops.request': '6/min',
        'upload': '3/min',
        'exams.request': '10/min',
        'config_exams.request': '12/min',
        'do_exams': '12/min',
        'sample_rates': '60/min',
    }
}
AUTH_USER_MODEL = 'account.User'
FORMAT_DATE = '%Y/%m/%d'
FORMAT_DATETIME = '%Y/%m/%d %X'
X_CHATWORKTOKEN = env_config('X_CHATWORKTOKEN')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.common.authentication_backend.SettingsBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
]

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {

        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        },
    },
}

# Email
EXPIRING_TOKEN_DURATION = datetime.timedelta(days=1)
EMAIL_HOST = env_config('EMAIL_HOST')
EMAIL_BACKEND = env_config('EMAIL_BACKEND')
EMAIL_PORT = env_config('EMAIL_PORT')
EMAIL_HOST_USER = env_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env_config('EMAIL_USE_TLS', cast=bool)
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Queue config ( Redis - rabbitmq )
CELERY_BROKER_URL = env_config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# social auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_config(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env_config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env_config('SOCIAL_AUTH_FACEBOOK_SECRET')

# phone verification
PHONE_VERIFICATION = {
    "BACKEND": "phone_verify.backends.twilio.TwilioBackend",
    "OPTIONS": {
        "SID": env_config('SID_PHONE'),
        "SECRET": env_config('SECRET_PHONE'),
        "FROM": env_config('FROM_PHONE'),
    },
    "TOKEN_LENGTH": 6,
    "MESSAGE": "Welcome to {app}! Please use security code {security_code} to proceed.",
    "APP_NAME": "Phone Verify",
    "SECURITY_CODE_EXPIRATION_TIME": 60,
    "VERIFY_SECURITY_CODE_ONLY_ONCE": True,
}

# jwt
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=3000),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': 'JWT',
}

# fcm
FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "test",
    "FCM_SERVER_KEY": env_config('FCM_SERVER_KEY'),
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
}

# logs
LOG_VIEWER_FILES = ['debug.log']
LOG_VIEWER_FILES_PATTERN = '*.log'
LOG_VIEWER_FILES_DIR = os.path.join(BASE_DIR, 'logs')
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_PAGE_LENGTH = 25  # total log lines per-page
LOG_VIEWER_PATTERNS = [']OFNI[', ']GUBED[',
                       ']GNINRAW[', ']RORRE[', ']LACITIRC[']
LOG_VIEWER_FILE_LIST_TITLE = "Custom title"
LOG_VIEWER_FILE_LIST_STYLES = "/static/css/my-custom.css"
os.makedirs('logs', exist_ok=True)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/debug.log',
#             'formatter': 'standard'
#         },
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/default.log',
#             'formatter': 'standard',
#         },
#         'request_debug_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/request_debug.log',
#             'formatter': 'standard',
#         },
#         'request_error_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/request_error.log',
#             'formatter': 'standard',
#         },
#         'mail_admins_handler': {
#             'level': 'DEBUG',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'email_backend': 'django.core.mail.backends.smtp.EmailBackend'
#         },
#     },
#     'root': {
#         'handlers': ['default'],
#         'level': 'DEBUG'
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': [
#                 'default',
#                 'request_debug_handler',
#                 'request_error_handler',
#                 'mail_admins_handler'
#             ],
#             'propagate': False
#         },
#         'django': {
#             'handlers': [
#                 'console',
#             ],
#             'propagate': False
#         },
#     }
# }

# reset password
RESET_PASSWORD_CODE_LENGTH = env_config('RESET_PASSWORD_CODE_LENGTH', cast=int)
RESET_PASSWORD_CODE_EXPIRATION_TIME = env_config(
    'RESET_PASSWORD_CODE_EXPIRATION_TIME', cast=int)
RESET_PASSWORD_EXPIRATION_TIME = env_config(
    'RESET_PASSWORD_EXPIRATION_TIME', cast=int)
LINK_RESET_PASSWORD = env_config('LINK_RESET_PASSWORD')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'NAME': ('', 'name', str),
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch://user:pass@localhost:9200'
    },
}

if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
    )

# connect mongodb
if os.environ.get("DATABASE_MONGO_URI"):
    connect(host=os.environ.get("DATABASE_MONGO_URI"))
