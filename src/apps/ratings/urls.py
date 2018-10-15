from django.conf.urls import include, url

from .api import urls as api_urls

app_name = 'ratings'

# API
urlpatterns = [

    # Votar el anuncio.
    url(r'^api/', include(api_urls)),
]
