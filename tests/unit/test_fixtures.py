from django.contrib.sites.models import Site

from alerts.models import AlertAnuncio

from .base_test import BaseTestCase


class FixturesTest(BaseTestCase):
    """Comprueba que los fixtures se han creado."""

    def test_users(self):
        """Numero de usuarios."""
        # Numero de usuarios.
        users = self.user_model.objects.all()
        self.assertEqual(users.count(), 2)

        # Usuario snicoper
        user = self.user_model.objects.get(pk=1)
        self.assertEqual(user.username, 'snicoper')
        self.assertEqual(user.email, 'snicoper@snicoper.local')
        self.assertTrue(self.login())
        self.assertEqual(user.first_name, 'Salvador')
        self.assertEqual(user.last_name, 'Nicolas')
        self.assertFalse(user.is_premium)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Usuario snicoper
        user = self.user_model.objects.get(pk=2)
        self.assertEqual(user.username, 'perico')
        self.assertEqual(user.email, 'snicoper@gmail.com')
        self.assertTrue(self.login(username='perico', password='123'))
        self.assertEqual(user.first_name, 'Perico')
        self.assertEqual(user.last_name, 'Palotes')
        self.assertFalse(user.is_premium)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_sites(self):
        """Sites se ha restaurado."""
        site = Site.objects.get(pk=1)

        self.assertEqual(site.name, 'OferVivienda')
        self.assertEqual(site.domain, '127.0.0.1:8000')

    def test_anuncios(self):
        """Anuncios se han cargado."""
        self.assertTrue(self.anuncio_model.objects.count() > 10)

    def test_alerts(self):
        """Alerts se han cargado, solo 2."""
        self.assertTrue(AlertAnuncio.objects.count() == 2)

        # Requiere 1 alert de snicoper y otra de perico
        try:
            snicoper = AlertAnuncio.objects.get(pk=1)
            perico = AlertAnuncio.objects.get(pk=2)

            self.assertEqual(snicoper.owner.username, 'snicoper')
            self.assertEqual(perico.owner.username, 'perico')
        except:
            self.fail('Es necesario al menos dos alerts, una para perico otra para snicoper')
