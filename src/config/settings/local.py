# flake8: noqa
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*h-nj!a*9r74ael028l53*u$5299g5k)kzaw@0+@e920+@-owh'

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.100']

# Application definition
THIRD_PARTY_APPS += (
    'debug_toolbar',
    'django_extensions',
)

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'oferviviendadev',
        'USER': 'snicoper',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/local')

# Email
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
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'snicoper'
EMAIL_HOST_PASSWORD = ''

# API KEY Google Maps, solo usada para desarrollo y tests
GMAPS_APIKEY = ''
GMAPS_APIKEY_PYTHON = ''

# PayPal
# sanbox|live
PAYPAL_FORM_ACTION = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
PAYPAL_RECEIVER_EMAIL = 'snicoper-facilitator@gmail.com'

# Mostrar fake adsense? muestra unas imagenes en su lugar.
ADSENSE_IMAGES_FAKE = False
