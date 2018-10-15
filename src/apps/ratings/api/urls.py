from django.conf.urls import url

from . import views as api_views

# API
urlpatterns = [

    # Votar el anuncio.
    url(
        regex=r'^rating/(?P<anuncio_id>\d+)/',
        view=api_views.AnuncioRatingApiView.as_view(),
        name='api_rating_anuncio'
    ),
]
