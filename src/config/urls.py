from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

from anuncios.sitemaps import AnunciosSitemap
from blog.sitemaps import BlogSitemap
from search.views import IndexSearchView
from utils.api import UserIpInfoApiView

# Sitemaps
sitemaps = {
    'anuncios': AnunciosSitemap,
    'blog': BlogSitemap
}

urlpatterns = [
    ##################################################
    # / Home page.
    url(r'^$', IndexSearchView.as_view(), name='home_page'),
    ##################################################

    # /accounts/*
    url(r'^accounts/', include('accounts.urls')),

    # /alerts/*
    url(r'^alerts/', include('alerts.urls')),

    # /anuncios/*
    url(r'^anuncios/', include('anuncios.urls')),

    # /auth/*
    url(r'^auth/', include('authentication.urls')),

    # /blog/*
    url(r'^blog/', include('blog.urls')),

    # /contact/*
    url(r'^contact/', include('contact.urls')),

    # /favorites/*
    url(r'^favorites/', include('favorites.urls')),

    # /images/*
    url(r'^gallery/', include('gallery.urls')),

    # /pages/*
    url(r'^pages/', include('pages.urls')),

    # /payments/*
    url(r'^payments/', include('payments.urls')),

    # /pmessages/*
    url(r'^pmessages/', include('pmessages.urls')),

    # /promos/*
    url(r'^promos/', include('promos.urls')),

    # /rating/*
    url(r'^ratings/', include('ratings.urls')),

    # /recommend/*
    url(r'^recommend/', include('recommend.urls')),

    # /recommend/*
    url(r'^search/', include('search.urls')),

    # /stats/*
    url(r'^stats/', include('stats.urls')),

    # /api-auth/*
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # /admin/*
    url(r'^sadmin/', admin.site.urls),
]

# Sitemaps para anuncios y blog.
urlpatterns.append(
    url(
        regex=r'^sitemap\.xml$',
        view=sitemap,
        kwargs={'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
)

# API
urlpatterns.append(

    # Obtener información de localización con la ip del usuario.
    # src/static/src/js/gmaps/geolocation.js
    # IMPORTANTE: Si se cambia el name, cambiarlo en el .js
    url(
        regex=r'^api/user-ip-info/$',
        view=UserIpInfoApiView.as_view(),
        name='api_user_ip_info'
    ),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    import debug_toolbar

    urlpatterns += [
        # /media/:<mixed>path/
        url(
            regex=r'^media/(?P<path>.*)$',
            view=serve,
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),

        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# Si se pone en DEBUG = False en desarrollo, para poder ver los static files.
# Muy importante, comentar cuando se termine.
# urlpatterns += [
#     url(
#         r'^media/(?P<path>.*)$',
#         serve,
#         {'document_root': settings.MEDIA_ROOT}
#     ),
#
#     url(
#         r'^static/(?P<path>.*)$',
#         serve,
#         {'document_root': settings.STATIC_ROOT}
#     ),
# ]
