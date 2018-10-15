from django.conf.urls import include, url

from . import views
from .api import urls as api_urls

app_name = 'favorites'

urlpatterns = [

    # Lista de favoritos de un usuario.
    url(
        regex=r'^list/$',
        view=views.FavoritesListView.as_view(),
        name='list'
    ),

    # Limpia la lista de favoritos
    url(
        regex=r'^delete/all/$',
        view=views.FavoriteUserListDeleteView.as_view(),
        name='delete_all'
    ),

    # API
    url(r'^api/', include(api_urls)),
]
