from django.conf import settings
from django.db import models

from anuncios.models import Anuncio


class Favorites(models.Model):
    """Anuncios favoritos de un usuario.

    El objeto relacional con User, se crea con un signal accounts.signals.
    """
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuario',
        related_name='favorites_user',
        on_delete=models.CASCADE,
        primary_key=True
    )
    anuncios = models.ManyToManyField(
        Anuncio,
        verbose_name='Anuncio',
        related_name='favorites_anuncios'
    )
