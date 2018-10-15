# flake8: noqa
from .base import *

# Añadir ~/tests a PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), 'tests'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l79pbxqzr9+8fzjz^@@smfo3k1ah3sq28we745k0bb5w_^pbgd'

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1']

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_django',
        'USER': 'test_django',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/test')

# Emails
DEFAULT_FROM_EMAIL = 'webmaster@snicoper.local'

# Admins
ADMINS = (
    ('Salvador Nicolas', 'snicoper@snicoper.local'),
)

# Grupos de email.
GROUP_EMAILS = {
    "NO-REPLY": 'no-responder@snicoper.local <snicoper@snicoper.local>',
    'CONTACTS': (
        'Salvador Nicolas <snicoper@snicoper.local>',
    ),
}

# SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.snicoper.local'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'snicoper'
EMAIL_HOST_PASSWORD = ''

# API KEY Google Maps, solo usada para desarrollo y tests
GMAPS_APIKEY = ''
GMAPS_APIKEY_PYTHON = ''

# PayPal
# sanbox|live
PAYPAL_FORM_ACTION = 'http://127.0.0.1:5000/'
PAYPAL_RECEIVER_EMAIL = 'snicoper-facilitator@gmail.com'
