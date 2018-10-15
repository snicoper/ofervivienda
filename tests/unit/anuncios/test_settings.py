from django.test import TestCase

from anuncios import settings as anuncios_settings


class AnuncioSettingsTest(TestCase):

    def test_valores_de_constantes(self):
        """Comprueba el valor de las constantes en settings."""
        self.assertEqual(anuncios_settings.ANUNCIO_DAYS_ACTIVE, 999)
        self.assertEqual(anuncios_settings.ANUNCIO_PAGINATE_BY, 12)
        self.assertEqual(anuncios_settings.ANUNCIO_MAX_ANUNCIOS, 3)
        self.assertEqual(anuncios_settings.ANUNCIO_NUM_RELACIONADIO, 6)
        self.assertEqual(anuncios_settings.ANUNCIO_RELACIONADO_KMS, 3)
        self.assertEqual(anuncios_settings.ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT, 3)
