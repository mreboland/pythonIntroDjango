"""
Django settings for learningLog project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+j^4v$7hmef@wn#^w5!gd!=s008$4!d+hl8qugp-hknv5x3_qk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


# Activating Models
# To use our models, we have to tell django to include our app in the overall project.
# It's important to place our own apps before the default apps in case we need to override any behaviour of the default apps with our own, custom behaviour.

# Next we need to tell django to modify the database so it can store info related to the model 'Topic'. From the terminal run:

# (ll_env)learning_log$ python manage.py makemigrations learningLogs
# Migrations for 'learning_logs':
# learning_logs/migrations/0001_initial.py
# - Create model Topic
# (ll_env)learning_log$

# makemigrations tells django to figure out how to modify the database so it can store the data associated with any new models we've define. The output here shows that Django has created a
# migration file called 0001_initial.py. This migration will create a table for the model Topic
# in the database.
# Now we’ll apply this migration and have Django modify the database for us:

# (ll_env)learning_log$ python manage.py migrate
# Operations to perform:
# Apply all migrations: admin, auth, contenttypes, learning_logs, sessions
# Running migrations:
# Applying learning_logs.0001_initial... OK

# Most of the output from this command is identical to the first time we issued the migrate command.
# The line we need to check appears at the end, where Django confirms that the migration for
# learning_logs worked OK. Whenever we want to modify the data that Learning Log manages, we’ll
# follow these three steps: modify models.py, call makemigrations on learning_logs, and tell Django to migrate the project.

# The django admin site

# Setting up superuser
# python manage.py createsuperuser
# Follow the prompts to set up a admin user for our site.



INSTALLED_APPS = [
    # My apps
    "learningLogs",
    "users",
    
    # Third party apps
    "bootstrap4",
    
    
    # Default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
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

ROOT_URLCONF = 'learningLog.urls'

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

WSGI_APPLICATION = 'learningLog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# My settings
LOGIN_URL = "users:login"