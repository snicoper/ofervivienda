from django.conf import settings
from django.db import models

from anuncios.models import Anuncio

from .managers import RatioManager


class Ratio(models.Model):
    """Puntuaciones de los anuncios."""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='ratio_user'
    )
    anuncio = models.ForeignKey(
        to=Anuncio,
        on_delete=models.CASCADE,
        verbose_name='anuncios',
        related_name='ratio_anuncio'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Puntuación'
    )

    objects = RatioManager()

    class Meta:
        verbose_name = 'Ratio'
        verbose_name_plural = 'Ratios'
        unique_together = (('user', 'anuncio'),)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.anuncio.get_title)
