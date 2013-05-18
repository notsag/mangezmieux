#-*- coding: utf-8 -*-
# Django settings for mangezmieux project.
import os
import django

#SESSIONS
SESSION_SAVE_EVERY_REQUEST = True

# DEBUG
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# ADMIN
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
SECRET_KEY = 'nm0lvt2y=)b836db1y=u+cvi77a0vic&p3c75ols(9&bcjp7g+'



# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mangez_mieux',    
        'USER': 'root',            
        'PASSWORD': 'root',        
        'HOST': 'localhost',       
        'PORT': '',
	'OPTIONS' : {
	    "init_command" : "SET storage_engine=MyISAM",
	}
    }
}


# Internationalisation
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = True # Internationalisation
USE_L10N = True # Formatage des dates et nombres en fonction de la locale
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SITE_ID = 1

# Chemins HTML, CSS, JS et Upload
MEDIA_ROOT = os.path.join(SITE_ROOT, 'upload/')
MEDIA_URL = '/upload/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates2/'),
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# URLs primaires
ROOT_URLCONF = 'urls'

# Modules installés
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rest_framework',
	'rest_framework.authtoken',
    'core',
    'home',
    'produit',
    'recette',
    'planning',
    'auth',
    'api',
    'mysqlfulltextsearch',
    'panier',
    'commande',
)


# AUTH module
AUTH_PROFILE_MODULE = 'auth.ProfilUtilisateur'
LOGIN_REDIRECT_URL = '/mon_compte'

# API module
REST_FRAMEWORK = {
		'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
		'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication','rest_framework.authentication.TokenAuthentication'),
		'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}


# LOG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
