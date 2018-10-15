import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add BASE_DIR and BASE_DIR/apps to $PYTHONPATH
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'django.contrib.gis',
)

THIRD_PARTY_APPS = (
    'rest_framework',
)

LOCAL_APPS = (
    'accounts.apps.AccountsConfig',
    'alerts.apps.AlertsConfig',
    'anuncios.apps.AnunciosConfig',
    'authentication.apps.AuthenticationConfig',
    'blog.apps.BlogConfig',
    'contact.apps.ContactConfig',
    'djtemplateforms.apps.DjtemplateformsConfig',
    'favorites.apps.FavoritesConfig',
    'gallery.apps.GalleryConfig',
    'localization.apps.LocalizationConfig',
    'pages.apps.PagesConfig',
    'payments.apps.PaymentsConfig',
    'pmessages.apps.PmessagesConfig',
    'promos.apps.PromosConfig',
    'ratings.apps.RatingsConfig',
    'recommend.apps.RecommendConfig',
    'search.apps.SearchConfig',
    'stats.apps.StatsConfig',
    'utils.apps.UtilsConfig',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.common_template_vars',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
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
LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Site
SITE_ID = 1

# Static files (CSS, JavaScript, Images) #
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media #
MEDIA_URL = '/media/'

# Users #
AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/auth/login/'

AUTHENTICATION_BACKENDS = (
    'authentication.backends.EmailOrUsernameModelBackend',
)

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
}

# Fixtures
FIXTURE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'fixtures'),
)

# Protocol, por defecto http
# Usar siempre request.is_secure()
# Este solo es por si se ha de acceder desde models u otro sitio mas inaccesible.
PROTOCOL = 'http'

# djtemplateforms
DJTEMPLATEFORMS_DEFAULT_TEMPLATE = 'bootstrap4'
