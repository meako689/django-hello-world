from hello42.settings import *
TESTFILES_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TESTFILES_DIR, 'db.sqlite3'),
    }
}
