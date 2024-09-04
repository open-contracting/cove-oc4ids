"""
Django settings for cove_project project.

Generated by 'django-admin startproject'.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from cove import settings

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# We use the setting to choose whether to show the section about Sentry in the
# terms and conditions
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import ignore_logger

    ignore_logger("django.security.DisallowedHost")
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

FATHOM = {
    "domain": os.getenv("FATHOM_ANALYTICS_DOMAIN", "cdn.usefathom.com"),
    "id": os.getenv("FATHOM_ANALYTICS_ID", ""),
}
VALIDATION_ERROR_LOCATIONS_LENGTH = settings.VALIDATION_ERROR_LOCATIONS_LENGTH
VALIDATION_ERROR_LOCATIONS_SAMPLE = settings.VALIDATION_ERROR_LOCATIONS_SAMPLE
DELETE_FILES_AFTER_DAYS = int(os.getenv("DELETE_FILES_AFTER_DAYS", 90))

# We can't take MEDIA_ROOT and MEDIA_URL from cove settings,
# ... otherwise the files appear under the BASE_DIR that is the Cove library install.
# That could get messy. We want them to appear in our directory.
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/infrastructure/media/"

SECRET_KEY = os.getenv("SECRET_KEY", "2n5k63x#a(xc@-!tpxisd)bd!3bimfr1prj-*t7tnl(*j+#$0k")
DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap3",
    "cove",
    "cove.input",
    "cove_oc4ids",
]


MIDDLEWARE = (
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "cove.middleware.CoveConfigCurrentApp",
    "django.middleware.cache.FetchFromCacheMiddleware",
)


ROOT_URLCONF = "cove_project.urls"

TEMPLATES = settings.TEMPLATES
TEMPLATES[0]["DIRS"] = [BASE_DIR / "cove_project" / "templates"]
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "cove_project.context_processors.from_settings",
)

WSGI_APPLICATION = "cove_project.wsgi.application"

# We can't take DATABASES from cove settings,
# ... otherwise the files appear under the BASE_DIR that is the Cove library install.
# That could get messy. We want them to appear in our directory.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("DB_NAME", str(BASE_DIR / "db.sqlite3")),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = settings.LANGUAGE_CODE
TIME_ZONE = settings.TIME_ZONE
USE_I18N = settings.USE_I18N
USE_TZ = settings.USE_TZ

LANGUAGES = settings.LANGUAGES

LOCALE_PATHS = (BASE_DIR / "cove_oc4ids" / "locale",)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# We can't take STATIC_URL and STATIC_ROOT from cove settings,
# ... otherwise the files appear under the BASE_DIR that is the Cove library install.
# and that doesn't work with our standard Apache setup.
STATIC_URL = "infrastructure/static/"
STATIC_ROOT = BASE_DIR / "static"

# Misc

LOGGING = settings.LOGGING
LOGGING["handlers"]["null"] = {
    "class": "logging.NullHandler",
}
LOGGING["loggers"]["django.security.DisallowedHost"] = {
    "handlers": ["null"],
    "propagate": False,
}

# OC4IDS Config

COVE_CONFIG = {
    # lib-cove-web options
    "app_name": "cove_oc4ids",
    "app_base_template": "cove_oc4ids/base.html",
    "app_verbose_name": "Open Contracting for Infrastructure Data Standards Review Tool",
    "app_strapline": "Review your OC4IDS data.",
    "input_methods": ["upload", "url", "text"],
    "support_email": "data@open-contracting.org",
}

# Because of how the standard site proxies traffic, we want to use this
USE_X_FORWARDED_HOST = True

# This Cove is served from the same domain as another Django app.
# To make sure sessions and CSRF tokens don't clash, use different names.
# https://github.com/open-contracting/deploy/issues/188
CSRF_COOKIE_NAME = "oc4idscsrftoken"
SESSION_COOKIE_NAME = "oc4idssessionid"

if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": "127.0.0.1:11211",
        }
    }
