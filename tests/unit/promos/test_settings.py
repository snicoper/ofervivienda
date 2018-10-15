from django.test import TestCase

from promos import settings as promos_settings


class PromosSettingsTest(TestCase):

    def test_settings(self):
        """Prueba settings.py."""
        self.assertEqual(promos_settings.PROMO_EXPIRE_DAYS, 30)
