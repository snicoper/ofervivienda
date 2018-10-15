from django.conf.urls import url

from . import views

app_name = 'pmessages'

urlpatterns = [

    # Lista de mensajes recibidos.
    url(
        regex=r'^inbox/$',
        view=views.MessageInboxView.as_view(),
        name='inbox'
    ),

    # Lista de mensajes enviados.
    url(
        regex=r'^outbox/$',
        view=views.MessageOutboxView.as_view(),
        name='outbox'
    ),

    # Lista de threads.
    url(
        regex=r'^thread/(?P<pk>\d+)/$',
        view=views.ThreadListView.as_view(),
        name='thread'
    ),

    # Crea un mensaje.
    url(
        regex=r'^create/$',
        view=views.MessageCreateView.as_view(),
        name='create'
    ),
]
