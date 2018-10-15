from django.conf.urls import url

from . import views as api_views

# API
urlpatterns = [

    # Obtener el usuario en JSON.
    url(
        regex=r'^user/$',
        view=api_views.GetUserFromFormGenerateCodeApiView.as_view(),
        name='api_get_user_in_form'
    ),
]
