"""
Django settings for emile project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY          = 'n)m)^6&^30w1ogm1$3=kkvs*9cbmxgqb-9y+1-o76jt4)4*5(j'
CSRF_COOKIE_SECURE  = False
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']

AUTHENTICATION_BACKENDS = ( 'web.backend.UserMobileBackend','django.contrib.auth.backends.ModelBackend', )

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16
}

# Application definitions
# Enviar email para esquecimento de senha
EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL  = ''
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'


INSTALLED_APPS = [
    #'material',
    #'material.frontend',
    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'web',
    'django_select2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'emile.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE   = 'PT-br'
TIME_ZONE       = 'America/Bahia'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True


#SUIT_CONFIG = {
    # header
    # 'ADMIN_NAME': 'Adminstração Emile',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
#}

# GRAPPELLI_ADMIN_TITLE = "Sistema de Administração do Emile Mobile"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
ADMIN_SITE_HEADER   = 'Sistema de Administração do Emile Mobile'
LOGIN_REDIRECT_URL  = 'web:home'
LOGOUT_URL          = 'web:login2'
STATIC_URL          = '/static/'
STATIC_ROOT         = os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_URL           = '/media/'
MEDIA_ROOT          = os.path.join(os.path.dirname(BASE_DIR), 'media')

PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_POST_URL'      : 'https://fcm.googleapis.com/fcm/send',
    'GCM_API_KEY'       : 'AIzaSyCDIZta44cPrrDxZvVLUm41Qs8jBcYwj54',
    # 'APNS_CERTIFICATE'  : MEDIA_ROOT + '/certificado/certifi.p12',
}
