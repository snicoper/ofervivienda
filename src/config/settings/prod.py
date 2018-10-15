# flake8: noqa
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l79pbxqzr9+8fzjz^@@smfo3k1ah3sq28we745k0bb5w_^pbgd'

ALLOWED_HOSTS = ['.ofervivienda.com']

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = 'ofervivienda.com'
SESSION_COOKIE_SECURE = True

# Application definition
THIRD_PARTY_APPS += ()

LOCAL_APPS += ()

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'oferviviendacom',
        'USER': 'oferviviendacom',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# TEMPLATE CONFIGURATION
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/prod')

# Email
# Email default.
DEFAULT_FROM_EMAIL = 'webmaster@ofervivienda.com'

# Donde mandara los errores, para mandar emails usar GROUP_EMAILS.
ADMINS = (
    ('Errors and security', 'weberrors@ofervivienda.com'),
)

# Grupos de email.
GROUP_EMAILS = {
    'NO-REPLY': 'OferVivienda.com <noreply@ofervivienda.com>',
    'CONTACTS': (
        'Salvador Nicolas <snicoper@ofervivienda.com>',
    ),
}

# SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'snicoper@gmail.com'
EMAIL_HOST_PASSWORD = ''

# Google Maps API KEY
GMAPS_APIKEY = ''
GMAPS_APIKEY_PYTHON = ''

# PayPal
# sanbox|live
PAYPAL_FORM_ACTION = 'https://www.paypal.com/cgi-bin/webscr'
PAYPAL_RECEIVER_EMAIL = 'snicoper@ofervivienda.com'

# Protocol, por defecto http
# Usar siempre request.is_secure()
# Este solo es por si se ha de acceder desde models u otro sitio mas inaccesible.
PROTOCOL = 'https'
