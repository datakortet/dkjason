# -*- coding: utf-8 -*-
import os

DIRNAME = os.path.dirname(__file__)


def pytest_configure():
    import django
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        TESTING=True,
        PRODUCTION=False,
        ROOT_URLCONF='urls',
        APPNAME='dkjason',
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': os.path.join(DIRNAME, 'cache'),
                'TIMEOUT': 60 * 60,
                'OPTIONS': {
                    'MAX_ENTRIES': 5000
                }
            }
        },
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(DIRNAME, 'testing.db'),
                # The following settings are not used with sqlite3:
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
        ),
        AUTH_USER_MODEL='auth.User'
    )
    django.setup()
