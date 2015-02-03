"""
Django settings for jaeweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6sa-8r^agj(tst-ggn%=7@_*o=_zuoqi3^(+1*vfntz-nherv('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jaeadmin',
    'pagination',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request"
)

ROOT_URLCONF = 'jaeweb.urls'

WSGI_APPLICATION = 'jaeweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jaeweb',
        'USER': 'jaeweb',
        'PASSWORD':'jaeweb',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard':{
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/jaeweb/jaeweb.log',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
	'django':{
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates/'),
)

#TIME_ZONE = 'CCT'

LANGUAGE_CODE = 'zh-cn'

#LOGIN_URL = "http://auth.jumeird.com/api/login?camefrom=ops_docker"
#app_key = "&app_key="
#app_name = "&app_name=ops_docker&key=1"
#auth_url = "http://auth.jumeird.com"
#auth_key = "481986a634ca11e4ab8c842b2b738d12"

LOGIN_URL = "http://auth.jumeird.com/api/login?camefrom=ops_docker"
app_key = "&app_key="
app_name = "&app_name=ops_docker&key=1"
auth_url = "http://auth.jumeird.com/"
auth_key = "481986a634ca11e4ab8c842b2b738d12"

BASE_URL="http://localhost:8282/v1"
