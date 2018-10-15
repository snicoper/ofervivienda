from django.conf.urls import url

from . import views as api_views

urlpatterns = [

    # Obtener posiciones de anuncios.
    url(
        regex=r'^anuncios/markers/$',
        view=api_views.SearchMarkersPositionsAPIView.as_view(),
        name='api_markers_positions'
    ),
]
