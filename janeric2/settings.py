"""
Django settings for janeric2 project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
if os.path.exists("env.py"):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY2', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEVELOPMENT2' in os.environ

ALLOWED_HOSTS = ['janeric2.herokuapp.com', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'home',
    'products',
    'cart',
    'checkout',
    'profiles',
    'localflavor',
    'phone_field',
    'crispy_forms',
    'storages',
    'shipping',
    'terms',
    'about',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "checkout.middleware.TimezoneMiddleware", #for local timezone code
]

ROOT_URLCONF = 'janeric2.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                #allauth needs this from django
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                'cart.contexts.cart_contents',
                ### other context_processors
                "checkout.context_processors.common_variables", #for local timezone code
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ],
            'libraries': {
                'cart_tools': 'cart.templatetags.cart_tools',
            }
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'janeric2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#if 'DATABASE_URL' in os.environ:
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
#else:
#    DATABASES = {
#       'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        }
#    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CLIENT_DEFAULT_TIME_ZONE = 'America/Los_Angeles'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


if 'USE_AWS' in os.environ:
    # Cache control
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    # Bucket Config
    AWS_STORAGE_BUCKET_NAME = 'janeric2'
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

CA_SALES_TAX = 7.75

STANDARD_SHIPPING_PERCENTAGE = 10
STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY2', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY2', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET2', '')

if 'DEVELOPMENT2' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'janericllc@example.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_FROM')

# Allauth email settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
LOGIN_URL = 'https://janeric2.herokuapp.com/accounts/login/'
LOGIN_REDIRECT_URL = 'https://janeric2.herokuapp.com/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Welcome to Janeric!  "
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_UNIQUE_EMAIL = True

