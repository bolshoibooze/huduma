from __future__ import absolute_import

import os.path
import djcelery
import datetime
djcelery.setup_loader()


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Artur', 'mwaigaryan@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'prototype',                      
        'USER': '',#25810687
        'PASSWORD': '',#bolshoi53
        'HOST': '',      
        'PORT': '',                    
    }
}


ALLOWED_HOSTS = []

TIME_ZONE = 'Africa/Nairobi'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1


USE_I18N = False

USE_L10N = False

USE_TZ = True


MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static/media/')

MEDIA_URL = '/static/media/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static'),
   
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


SECRET_KEY = ')wjbyzau_&68-3&+ja)4x*mgqrjiv3vz_ax8=(-s2&xf!(5l1e'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yawdadmin.middleware.PopupMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'huduma.urls'


WSGI_APPLICATION = 'huduma.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yawdadmin',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'accounts',
    'business',
    'livevalidation',
    'import_export',
    'ua_detector',
    'djcelery',
    'tastypie',
)

AUTH_USER_MODEL = 'accounts.CustomUser'

GENDER = (
   ('Male','Male'),
   ('Female','Female')
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


CELERYBEAT_SCHEDULE = {
    'unlock-unconfirmed-names': {
        'task': 'business.tasks.unlock_unconfirmed_names',
        'schedule': datetime.timedelta(hours=24)
    },
    
    'confirm-business-name': {
        'task': 'business.tasks.confirmed_name',
        'schedule': datetime.timedelta(seconds=1)
    },
    
    'update-reserved-names': {
        'task': 'business.tasks.update_reserved_names',
        'schedule': datetime.timedelta(seconds=1)
    },
    
    'update-registered-names': {
        'task': 'business.tasks.update_registered_names',
        'schedule': datetime.timedelta(seconds=1)
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
