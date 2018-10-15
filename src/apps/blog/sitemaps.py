from django.contrib.sitemaps import Sitemap

from .models import Article


class BlogSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.create_at
