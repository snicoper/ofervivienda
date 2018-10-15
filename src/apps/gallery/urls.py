from django.conf.urls import url

from . import views

app_name = 'gallery'

urlpatterns = [

    # Muestra las imágenes asociadas a un anuncio.
    url(
        regex=r'^list/anuncio(?P<id_anuncio>\d+)/$',
        view=views.ImageAnuncioListView.as_view(),
        name='anuncio_gallery_list'
    ),

    # Añadir imágenes perteneciente a anuncio.
    url(
        regex=r'^add/anuncio(?P<id_anuncio>\d+)/$',
        view=views.ImageAnuncioCreateView.as_view(),
        name='image_anuncio_add'
    ),

    # Actualizar/Cambiar una imagen.
    url(
        regex=r'^update/image(?P<pk>\d+)/$',
        view=views.ImageAnuncioUpdateView.as_view(),
        name='image_anuncio_update'
    ),

    # Eliminar una imagen.
    url(
        regex=r'^delete/image(?P<pk>\d+)/$',
        view=views.ImageAnuncioDeleteView.as_view(),
        name='image_anuncio_delete'
    ),
]
