from django.conf.urls import url

from . import views

app_name = 'recommend'

urlpatterns = [

    # Form para recomendar anuncio.
    url(
        regex=r'^anuncio/(?P<anuncio_id>\d+)/$',
        view=views.RecommendAnuncioIndexView.as_view(),
        name='anuncio'
    ),
]
