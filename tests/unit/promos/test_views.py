from django.core import mail
from django.urls import reverse

from payments.models import PaymentIpn
from promos import settings as promos_settings

from .base_promos import BasePromoTest


class GenerateCodePromoViewTest(BasePromoTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'promos:generate_code_promo'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)
        self.form_data = {
            'to_user': 2,
            'payment_promo': PaymentIpn.PREMIUM6,
        }

    def test_usuario_anonimo_302(self):
        """Un usuario anónimo lanza 404."""
        self.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_usuario_login_200(self):
        """Un usuario logueado, status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'promos/create_code_promo.html')

    def test_context_data(self):
        """Prueba las variables de contexto."""
        context = self.response.context

        # Dias de expiración de la promo.
        self.assertEqual(context['promo_expire_days'], promos_settings.PROMO_EXPIRE_DAYS)

    def test_post_genera_codigo_OK(self):
        """Genera un código de promoción valido."""
        # Se asegura que no hay ninguna promo en la db.
        promos_count = self.promo_model.objects.count()
        self.assertEqual(promos_count, 0)

        # No hay ningún email en la bandeja.
        self.assertEqual(len(mail.outbox), 0)

        # Manda un formulario valido.
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)

        # La db ha incrementado en 1.
        new_promos_count = self.promo_model.objects.count()

        self.assertEqual(new_promos_count, promos_count + 1)

        # Prueba los datos generados en la db.
        promo = self.promo_model.objects.first()

        self.assertEqual(len(promo.code), 12)
        self.assertEqual(
            promo.payment_promo,
            PaymentIpn.PREMIUM6
        )

        # Prueba que aun no se ha usado.
        self.assertFalse(promo.active)

        # Se ha enviado el email.
        self.assertEqual(len(mail.outbox), 1)


class PromoValidateCodeViewTest(BasePromoTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'promos:validate'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)
        self.promo = self.promo_model.objects.create(
            payment_promo=PaymentIpn.ANUNCIO
        )

    def test_usuario_anonimo_302(self):
        """Un usuario anónimo, lo redirecciona a login."""
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )
        self.logout()
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_usuario_login_200(self):
        """Un usuario logueado, status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'promos/validate_code.html')

    def test_post_form_valid(self):
        """Prueba method POST en el form."""
        response = self.client.post(self.url, data={'code': self.promo.code}, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:profile'),
            status_code=302,
            target_status_code=200
        )

    def test_usuario_anadido_la_promocion(self):
        """El usuario ahora tiene un anuncio premium."""
        self.client.post(self.url, data={'code': self.promo.code})
        user = self.user_model.objects.get(pk=1)

        self.assertEqual(user.anuncios_premium, 1)
