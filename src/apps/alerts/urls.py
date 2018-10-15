from django.conf.urls import url

from . import views

app_name = 'alerts'

urlpatterns = [

    # Detalles de una alerta.
    url(
        regex=r'^$',
        view=views.AlertUserListView.as_view(),
        name='list'
    ),

    # Detalles de una alerta.
    url(
        regex=r'^details/(?P<pk>\d+)/$',
        view=views.AlertDetailsView.as_view(),
        name='details'
    ),

    # Añadir una nueva alerta.
    url(
        regex=r'^add/(?P<category>[a-z]+)/$',
        view=views.AlertCreateView.as_view(),
        name='create'
    ),

    # Actualizar una alerta.
    url(
        regex=r'^update/(?P<pk>\d+)/$',
        view=views.AlertUpdateView.as_view(),
        name='update'
    ),

    # Elimina una alerta.
    url(
        regex=r'^delete/(?P<pk>\d+)/$',
        view=views.AlertDeleteView.as_view(),
        name='delete'
    ),

    # Elimina todas las alertas de un usuario.
    url(
        regex=r'^delete-all/$',
        view=views.AlertsAllDeleteView.as_view(),
        name='delete_all'
    ),
]
