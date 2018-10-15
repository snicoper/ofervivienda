from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [

    # Perfil privado de usuario.
    url(
        regex=r'^profile/$',
        view=views.UserProfileView.as_view(),
        name='profile'
    ),

    # Perfil público de usuario.
    url(
        regex=r'^(?P<slug>\w+)/profile/$',
        view=views.UserProfilePublicView.as_view(),
        name='profile_public'
    ),

    # Actualizar perfil.
    url(
        regex=r'^profile/update/$',
        view=views.UserProfileUpdateView.as_view(),
        name='profile_update'
    ),

    # Cambiar/añadir avatar de usuario.
    url(
        regex=r'^avatar/update/$',
        view=views.UserAvatarUpdateView.as_view(),
        name='avatar_update'
    ),

    # Detalles opciones de usuario.
    url(
        regex=r'^options/$',
        view=views.UserOptionsDetailView.as_view(),
        name='options'
    ),

    # Form actualiza opciones de usuario.
    url(
        regex=r'^options/update/$',
        view=views.UserOptionsUpdateView.as_view(),
        name='options_update'
    ),

    # Detalles localización del usuario.
    url(
        regex=r'^location/$',
        view=views.UserLocationDetailView.as_view(),
        name='location'
    ),

    # Actualizar localización del usuario.
    url(
        regex=r'^location/update/$',
        view=views.UserLocationUpdateView.as_view(),
        name='location_update'
    ),
]
