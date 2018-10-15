from django.conf.urls import url

from . import views

app_name = 'pages'

urlpatterns = [

    # Cookies Consent
    url(
        regex=r'^cookie-consent/$',
        view=views.CookieConsentView.as_view(),
        name='cookie_consent'
    ),
]
