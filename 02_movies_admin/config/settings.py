import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

include(
    'components/database.py',
    'components/templates.py',
    'components/apps.py',
    'components/middleware.py',
    'components/etc.py',
    'components/pass_validators.py',
)


ROOT_URLCONF = 'config.urls'


WSGI_APPLICATION = 'config.wsgi.application'


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

LOCALE_PATHS = ['movies/locale']

INTERNAL_IPS = ['127.0.0.1']
