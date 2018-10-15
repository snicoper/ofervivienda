from django.contrib.sitemaps import Sitemap

from .models import Anuncio


class AnunciosSitemap(Sitemap):
    changefreq = 'never'
    protocol = 'https'
    priority = 0.5

    def items(self):
        return Anuncio.objects.published()

    def lastmod(self, obj):
        return obj.create_at
