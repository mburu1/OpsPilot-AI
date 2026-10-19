from .base import *

DEBUG = True
# Use in-memory SQLite for tests to speed up CI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
