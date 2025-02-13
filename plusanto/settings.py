"""
Django settings for plusanto project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ

# Inicjalizacja pliku .env
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOGIN_URL = "/accounts/login/" # Ustawienie przekierowania do strony logowania


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Zmienić na False na serwerze
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '88.99.97.188'
]


# Application definition

INSTALLED_APPS = [
    # DjangoApps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Narzędzie do wczytywania statycznych plików
    'django.contrib.staticfiles',
    'debug_toolbar', # Narzędzie debugowania
    # MyApps
    'accounts', # Aplikacja obsługująca konta
    'main', # Główna aplikacja
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware', # Narzędzie do debugowania, działa jedynie na localhostcie
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Narzędzie do wczytywania statycznych plików
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Odczytuje język przeglądarki i dostosowuje stronę do tego języka

]

INTERNAL_IPS = [
    # ...
    '127.0.0.1', # Definiujemy IP localhosta
    # ...
]

ROOT_URLCONF = 'plusanto.urls'

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

WSGI_APPLICATION = 'plusanto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Silnik bazy danych django
        'NAME': env('DATABASE_NAME'),           # Nazwa bazy danych brana z pliku .env
        'USER': env('DATABASE_USER'),           # Nazwa użytkownika brana z pliku .env
        'PASSWORD': env('DATABASE_PASSWORD'),   # Hasło brane z pliku .env
        'HOST': 'localhost',                    # Adres serwera
        'PORT': '3306',                         # Port bazy danych
        'CHARSET': 'utf8_general_ci',           # Kodowanie tekstu

    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [ # Formy walidacji hasła
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pl-pl' # Język strony

TIME_ZONE = 'CET' # Strefa czasowa strony

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Definiowanie ścieżek plików statyczny oraz systemu ich obsługa w etapie produkcji
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
