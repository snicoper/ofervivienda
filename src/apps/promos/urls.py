from django.conf.urls import include, url

from . import views
from .api import urls as api_urls

app_name = 'promos'

urlpatterns = [

    # Genera y envía un código de promoción a un usuario.
    url(
        regex=r'^generate/code/$',
        view=views.GenerateCodePromoView.as_view(),
        name='generate_code_promo'
    ),

    # Validación del un código.
    url(
        regex=r'^validate/$',
        view=views.PromoValidateCodeView.as_view(),
        name='validate'
    ),

    # API
    url(r'^api/', include(api_urls)),
]
