from django.db import models


class ArticleManager(models.Manager):

    def published(self, **kwargs):
        """Solo los artículos que estén actives."""
        return self.get_queryset().filter(active=True, **kwargs)
