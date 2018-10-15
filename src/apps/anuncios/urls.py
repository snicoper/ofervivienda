from django.conf.urls import include, url

from . import views
from .api import urls as api_urls

app_name = 'anuncios'

urlpatterns = [

    # Lista publica de anuncios (Actualmente desactivada para los usuarios).
    url(
        regex=r'^$',
        view=views.AnuncioListView.as_view(),
        name='list'
    ),

    # Lista de anuncios por id usuario.
    url(
        regex=r'^(?P<slug>\w+)/list/$',
        view=views.AnuncioListByOwnerView.as_view(),
        name='list_by_owner'
    ),

    # Detalles de un anuncio.
    url(
        regex=r'^details/(?P<pk>\d+)/$',
        view=views.AnuncioDetailView.as_view(),
        name='details'
    ),

    # Pagina principal de creación de anuncios.
    url(
        regex=r'^create/$',
        view=views.AnuncioCreateSelectListView.as_view(),
        name='create_select'
    ),

    # Create anuncio.
    url(
        regex=r'^create/(?P<category>\w+)/$',
        view=views.AnuncioCreateView.as_view(),
        name='create'
    ),

    # Update anuncio.
    url(
        regex=r'^update/(?P<category>\w+)/(?P<pk>\d+)/$',
        view=views.AnuncioUpdateView.as_view(),
        name='update'
    ),

    # Marcar como active=False un anuncio.
    url(
        regex=r'^deactivate/(?P<id_anuncio>\d+)/$',
        view=views.AnuncioDeactivateView.as_view(),
        name='deactivate'
    ),

    # Marcar como active=False un anuncio.
    url(
        regex=r'^activate/(?P<id_anuncio>\d+)/$',
        view=views.AnuncioActivateView.as_view(),
        name='activate'
    ),

    # Marcar como active=False un anuncio.
    url(
        regex=r'^convert/premium/(?P<id_anuncio>\d+)/$',
        view=views.AnuncioConvertPremiumView.as_view(),
        name='convert_anuncio_premium'
    ),

    # API
    url(r'^api/', include(api_urls)),
]
