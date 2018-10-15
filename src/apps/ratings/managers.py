from django.db import models


class RatioManager(models.Manager):

    def get_ratio_for_anuncio(self, anuncio):
        """Obtener el ratio de un anuncio.

        Args:
            anuncio (Anuncio): Objeto Anuncio.

        Returns:
            float|int: Numero decimal en caso de tener media, 0 en caso de no tener
            ninguna punctuation.
        """
        ratio = self.get_queryset().filter(anuncio=anuncio).aggregate(models.Avg('score'))
        if ratio['score__avg']:
            return ratio['score__avg']
        return 0
