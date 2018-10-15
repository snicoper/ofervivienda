from django.conf.urls import url

from . import views

app_name = 'payments'

urlpatterns = [

    # Procesa un pago de cuenta Premium.
    url(
        regex=r'^account/premium/$',
        view=views.ProcessAccountPremiumView.as_view(),
        name='process_account_premium'
    ),

    # Procesa un pago de cuenta Premium.
    url(
        regex=r'^anuncio/premium/$',
        view=views.ProcessAnuncioPremiumView.as_view(),
        name='process_anuncio_premium'
    ),

    # Notifica pago con éxito de cuenta Premium.
    url(
        regex=r'^notify/account/premium/$',
        view=views.NotifyAccountPremiumView.as_view(),
        name='notify_account_premium'
    ),

    # Notifica pago con éxito de un anuncio Premium.
    url(
        regex=r'^notify/anuncio/premium/$',
        view=views.NotifyAnuncioPremiumView.as_view(),
        name='notify_anuncio_premium'
    ),

    # Pagina de retorno de PayPal.
    url(
        regex=r'^return/premium/$',
        view=views.ReturnView.as_view(),
        name='return_premium'
    ),
]
