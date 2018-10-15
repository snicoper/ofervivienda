"""
Notificaciones de distintas alertas.

En los fixtures solo tiene una alerta de snicoper, por lo que la alerta la ha
de crear perico.
"""
from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse

from tests.unit.base_test import BaseTestCase


class NotifyAlertsTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:create'
        self.url = reverse(
            self.urlconf,
            kwargs={'category': self.anuncio_model.HABITACION.lower()}
        )
        self.response = self.client.get(self.url)
        self.form_data = {
            "country": "Espa\u00f1a",
            "state": "Barcelona",
            "city": "Granollers",
            "address": "Ramon Llull 28 1\u00ba 1\u00ba",
            "zipcode": "08401",
            "owner": 2,
            "category": "HABITACION",
            "metros_cuadrados": None,
            "phone": "987654321",
            "precio": "200",
            "type_anuncio": "ALQUILER",
            "genero": "CHICOCHICA",
            "permite_fumar_piso": False,
            "permite_fumar_habitacion": True,
            "internet": False,
            "description": "",
            "is_premium": False,
            "latitude": 41.6140513,
            "longitude": 2.28780340000003
        }

    def test_post(self):
        """Test de la creación de una anuncio.

        Para que pase el test, requiere de que snicoper tenga una alerta de
        habitación en ramon llull en los fixtures.

        La data de este form, lo ha de crear perico, es una habitación.
        """
        # Snicoper como user premium para evitar problemas.
        user = self.user_model.objects.get(pk=2)
        user.is_premium = True
        user.save()
        self.login(user.username, '123')

        # Crear un anuncio nuevo.
        response = self.client.post(self.url, data=self.form_data, follow=True)
        last_id = self.anuncio_model.objects.order_by('id').last().id
        expected_url = reverse('gallery:image_anuncio_add', kwargs={'id_anuncio': last_id})

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Comprobar que se le ha mandado un Email a snicoper
        # sobre la alerta.
        current_site = Site.objects.get(pk=1)
        subject = 'Anuncio que puede interesarte desde {}'.format(current_site.name)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)

    def test_alertas_no_notifica_al_propio_usuario(self):
        """El anuncio lo crea el mismo usuario que debería recibir la alerta,
        por lo tanto, no la debería recibir.

        La alerta la manda snicoper, que es superuser.
        """
        self.login()
        self.form_data['owner'] = 1
        response = self.client.post(self.url, data=self.form_data)
        last_id = self.anuncio_model.objects.order_by('id').last().id
        expected_url = reverse('gallery:image_anuncio_add', kwargs={'id_anuncio': last_id})

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Comprobar que el email no se manda.
        self.assertEqual(len(mail.outbox), 0)
