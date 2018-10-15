from django.conf.urls import url

from . import views

app_name = 'contact'

urlpatterns = [

    # Form de contacto.
    url(
        regex=r'^$',
        view=views.ContactView.as_view(),
        name='contact'
    ),

    # Lista de mensajes de contacto.
    url(
        regex=r'^messages/$',
        view=views.ContactMessageListView.as_view(),
        name='message_list'
    ),

    # Detalles de un mensaje.
    url(
        regex=r'^message/(?P<pk>\d+)/$',
        view=views.ContactMessageDetailView.as_view(),
        name='message_detail'
    ),
]
