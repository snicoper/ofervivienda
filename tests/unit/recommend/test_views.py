from django import forms
from django.core import mail
from django.urls import reverse

from tests.unit.base_test import BaseTestCase


class RecommendAnuncioIndexViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.anuncio = self.anuncio_model.objects.get(pk=1)
        self.url = 'recommend:anuncio'
        self.urlconf = reverse(self.url, kwargs={'anuncio_id': self.anuncio.pk})
        self.login()
        self.response = self.client.get(self.urlconf)
        self.form_data = {
            'from_email': self.user.email,
            'email_to': 'email@example.com',
            'body': 'Message content',
        }

    def test_usuario_login_status_code_200(self):
        """Un usuario logueado, status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_anonimo_status_code_200(self):
        """Un usuario anónimo, status_code 200."""
        self.logout()
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 200)

    def test_usuario_login_from_email_con_su_usuario(self):
        """El usuario con login, el campo from_email es el del usuario."""
        self.assertEqual(self.response.context['form'].initial['from_email'], self.user.email)

    def test_usuario_anonimo_from_email_initial_no_existe(self):
        """Un usuario anónimo, el campo from email no tiene datos iniciales en
        el form.
        """
        self.logout()
        initial = self.client.get(self.urlconf).context['form'].initial

        self.assertNotIn('from_email', initial)

    def test_usuario_login_field_from_email_hiddeninput(self):
        """El usuario logueado, el widget form_valid es hidden."""
        widget = self.response.context['form'].fields['from_email'].widget

        self.assertIsInstance(widget, forms.HiddenInput)

    def test_context_data(self):
        """Prueba get_context_data."""
        context = self.response.context

        self.assertIn('anuncio', context)

        # El id de anuncio.
        anuncio_id = context['anuncio'].pk

        self.assertEqual(self.anuncio.pk, anuncio_id)

    def test_post_envia_el_email_y_redirecciona(self):
        """Cuando el form es valido, envía un email y redirecciona otra vez a
        detalles del anuncio.
        """
        response = self.client.post(self.urlconf, data=self.form_data, follow=True)
        expected_url = reverse('anuncios:details', kwargs={'pk': self.anuncio.pk})

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        self.assertEqual(len(mail.outbox), 1)
