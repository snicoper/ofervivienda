from django.conf.urls import include, url

from . import views
from .api import urls as api_urls

app_name = 'search'

urlpatterns = [

    # Búsquedas.
    url(
        regex=r'^$',
        view=views.SearchFiltersView.as_view(),
        name='search'
    ),

    # Búsquedas en una categoría concreta.
    url(
        regex=r'^(?P<category>[a-z]+)/$',
        view=views.SearchFiltersView.as_view(),
        name='search_category'
    ),

    # Busqueda con mapa.
    url(
        regex=r'^map/(?P<category>\w+)/$',
        view=views.SearchMapView.as_view(),
        name='map'
    ),

    # API
    url(r'^api/', include(api_urls)),
]
