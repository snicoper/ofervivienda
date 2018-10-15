from django.conf.urls import url

from . import views as api_views

# API
urlpatterns = [

    # Actualizar update_at del anuncio.
    url(
        regex=r'^update-at/(?P<pk>\d+)/$',
        view=api_views.AnuncioUpdateAtUpdateAPIView.as_view(),
        name='api_update_at'
    ),
]
