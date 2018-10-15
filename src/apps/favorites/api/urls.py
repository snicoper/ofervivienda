from django.conf.urls import url

from . import views as api_views

# API
urlpatterns = [

    # Añade un favorito.
    url(
        regex=r'^add/$',
        view=api_views.FavoritesAddApiView.as_view(),
        name='api_add'
    ),

    # Eliminar un favorito.
    url(
        regex=r'^remove/$',
        view=api_views.FavoritesRemoveApiView.as_view(),
        name='api_remove'
    ),
]
