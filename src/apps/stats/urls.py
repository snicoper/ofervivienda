from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [

    # Pagina principal de stats.
    url(
        regex=r'^$',
        view=views.AdminIndexView.as_view(),
        name='index'
    ),
]
