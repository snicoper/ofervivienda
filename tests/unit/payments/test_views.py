import os

from django.core import mail
from django.test import RequestFactory
from django.urls import reverse

from payments import settings as payments_settings
from payments.models import PaymentIpn

from .base_payments import BasePaymentIpnTest


class ProccessAccountPremiumViewTest(BasePaymentIpnTest):
    """Tests del view src/apps/payments/views.py."""

    def setUp(self):
        super().setUp()
        self.urlconf = 'payments:process_account_premium'
        self.user = self.user_model.objects.get(pk=1)

    def _login_and_get_response(self):
        """Loguea al usuario y obtener el response."""
        self.login()
        return self.client.get(reverse(self.urlconf))

    def test_status_code_302_usuario_anonimo(self):
        """El usuario anónimo no tiene acceso."""
        response = self.client.get(reverse(self.urlconf))
        self.assertEqual(response.status_code, 302)

    def test_status_code_200_usuario_logueado(self):
        """Un usuario logueado tiene acceso."""
        response = self._login_and_get_response()
        self.assertTrue(response.status_code, 200)

    def test_template_usado(self):
        """Template usado."""
        response = self._login_and_get_response()
        self.assertTemplateUsed(response, 'payments/process_account_premium.html')

    def test_variables_de_contexto(self):
        """Comprueba los valores de las variables de contexto."""
        response = self._login_and_get_response()
        context = response.context

        # card_info[0]
        card_info = context['card_info'][0]
        self.assertEqual(card_info['title'], '1 Mes Premium')
        self.assertEqual(card_info['body'], '')
        self.assertEqual(card_info['amount'], payments_settings.PAYMENTS_PREMIUM1)

        # forms[0]
        form = context['forms'][0]
        self.assertEqual(form['amount'].value(), self.payments_settings.PAYMENTS_PREMIUM1)
        self.assertEqual(form['item_name'].value(), self.choices.get('PREMIUM1'))
        self.assertEqual(form['item_number'].value(), PaymentIpn.PREMIUM1)
        self.assertTrue(len(form['invoice'].value()) > 10)
        self.assertEqual(form['custom'].value(), self.user.pk)
        self.assertEqual(form['cmd'].value(), '_xclick')
        self.assertEqual(form['business'].value(), self.test_settings.PAYPAL_RECEIVER_EMAIL)
        self.assertEqual(form['charset'].value(), 'utf-8')
        self.assertEqual(
            form['notify_url'].value(),
            'http://testserver{}'.format(reverse('payments:notify_account_premium'))
        )
        self.assertEqual(
            form['return'].value(),
            'http://testserver{}'.format(reverse('payments:return_premium'))
        )
        self.assertEqual(
            form['cancel_return'].value(),
            'http://testserver{}'.format(reverse('accounts:profile'))
        )


class ProcessAnuncioPremiumViewTest(BasePaymentIpnTest):
    """Tests ProcessAnuncioPremiumView."""

    def setUp(self):
        super().setUp()
        self.urlconf = 'payments:process_anuncio_premium'
        self.user = self.user_model.objects.get(pk=1)

    def _login_and_get_response(self):
        """Loguea al usuario y obtener el response."""
        self.login()
        return self.client.get(reverse(self.urlconf))

    def test_status_code_302_usuario_anonimo(self):
        """El usuario anónimo no tiene acceso."""
        response = self.client.get(reverse(self.urlconf))
        self.assertEqual(response.status_code, 302)

    def test_status_code_200_usuario_logueado(self):
        """Un usuario logueado tiene acceso."""
        response = self._login_and_get_response()
        self.assertTrue(response.status_code, 200)

    def test_template_usado(self):
        """Template usado."""
        response = self._login_and_get_response()
        self.assertTemplateUsed(response, 'payments/process_anuncio_premium.html')

    def test_variables_de_contexto(self):
        """Comprueba los valores de las variables de contexto."""
        response = self._login_and_get_response()
        context = response.context

        # card_info[0]
        card_info = context['card_info'][0]
        self.assertEqual(card_info['title'], 'Anuncio Premium')
        self.assertEqual(card_info['body'], '')
        self.assertEqual(
            card_info['amount'],
            payments_settings.PAYMENTS_ANUNCIO
        )

        # forms[0]
        form = context['forms'][0]
        self.assertEqual(form['amount'].value(), self.payments_settings.PAYMENTS_ANUNCIO)
        self.assertEqual(form['item_name'].value(), self.choices.get('ANUNCIO'))
        self.assertEqual(form['item_number'].value(), PaymentIpn.ANUNCIO)
        self.assertTrue(len(form['invoice'].value()) > 10)
        self.assertEqual(form['custom'].value(), self.user.pk)
        self.assertEqual(form['cmd'].value(), '_xclick')
        self.assertEqual(form['business'].value(), self.test_settings.PAYPAL_RECEIVER_EMAIL)
        self.assertEqual(form['charset'].value(), 'utf-8')
        self.assertEqual(
            form['notify_url'].value(),
            'http://testserver{}'.format(reverse('payments:notify_anuncio_premium'))
        )
        self.assertEqual(
            form['return'].value(),
            'http://testserver{}'.format(reverse('payments:return_premium'))
        )
        self.assertEqual(
            form['cancel_return'].value(),
            'http://testserver{}'.format(reverse('accounts:profile'))
        )


class NotifyPremiumViewTest(BasePaymentIpnTest):
    """Test NotifyAccountPremiumView.

    Se reproduce una emulación con los datos que envía PayPal.

    No he encontrado forma para probar las vistas asociadas a Notify.
    La única manera que veo es hacerlo desde PayPal Test IPN.
    """

    def test_http_get_no_permitido(self):
        """Http GET siempre redirecciona a '/'."""
        response = self.client.get(reverse('payments:notify_account_premium'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class SaveDataAccountPremiumNotify(BasePaymentIpnTest):
    """Prueba utils.save_data."""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_save_data(self):
        """Mandando los datos, debe cambiar el estado del usuario a premium.

        Prueba las funciones de src/apps/payments/utils.py:
            save_data()
            process_account_premium()
            notify_mail_account_premium()
        """
        data = self.data_json['PREMIUM1']
        request = self.factory.get('/')
        request.POST = data
        copy_expire_premium_at = self.user_model.objects.get(pk=1).expire_premium_at

        # Guarda los datos en PaymentIpn.
        ipn = self.payments_utils.save_data(request)
        self.assertIsInstance(ipn, self.payments_model)
        self.assertEqual(self.payments_model.objects.count(), 1)

        # Procesa la cuenta y cambia el estado a premium del usuario.
        user = self.payments_utils.process_account_premium(ipn)
        self.assertIsInstance(user, self.user_model)
        self.assertTrue(user.is_premium)
        self.assertTrue(copy_expire_premium_at < user.expire_premium_at)

        # Comprueba que el Email ha sido enviado
        self.payments_utils.notify_mail_account_premium(request, ipn)
        self.assertEqual(len(mail.outbox), 1)


class SaveDataAnuncioPremiumNotify(BasePaymentIpnTest):
    """Prueba utils.save_data."""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_save_data(self):
        """Mandando los datos, debe cambiar el estado del usuario a Premium.

        Prueba las funciones de src/apps/payments/utils.py:
            save_data()
            process_anuncio_premium()
            notify_mail_anuncio_premium()
        """
        data = self.data_json['ANUNCIO']
        request = self.factory.get('/')
        request.POST = data

        # Guarda los datos en PaymentIpn.
        ipn = self.payments_utils.save_data(request)
        self.assertIsInstance(ipn, self.payments_model)
        self.assertEqual(self.payments_model.objects.count(), 1)

        # Procesa la cuenta y aumenta en 1 user.anuncios_premium.
        user = self.payments_utils.process_anuncio_premium(ipn)
        self.assertIsInstance(user, self.user_model)
        self.assertEqual(user.anuncios_premium, 1)

        # Comprueba que el Email ha sido enviado
        self.payments_utils.notify_mail_anuncio_premium(request, ipn)
        self.assertEqual(len(mail.outbox), 1)


class ReturnViewTest(BasePaymentIpnTest):
    """Pruebas ReturnView."""

    def setUp(self):
        super().setUp()
        self.reverse = reverse('payments:return_premium')
        self.data = self.data_json['PREMIUM1']

    def test_get_redirecciona_a_inicio(self):
        """Http POST redirecciona a '/'."""
        response = self.client.get(self.reverse)
        self.assertEqual(response.status_code, 302)

    def test_post_sin_datos_redirecciona_a_inicio(self):
        """Sin datos en POST redirecciona a inicio.

        Se supone que la redirección se hace desde PayPal y
        devuelve datos vía POST.
        """
        response = self.client.post(self.reverse)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_post_status_code_200(self):
        """Http POST status_code 200."""
        response = self.client.post(self.reverse, data=self.data)
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Template usado."""
        response = self.client.post(self.reverse, data=self.data)
        self.assertTemplateUsed(response, 'payments/return.html')


class WriteLogErrorsTest(BasePaymentIpnTest):
    """Comprueba write_log_errors()."""

    def setUp(self):
        super().setUp()
        base_root = os.path.dirname(self.test_settings.BASE_DIR)
        log_dir = os.path.join(base_root, 'logs')
        self.filepath = '{}/paypal.log'.format(log_dir)
        self.errors = [
            'mi error 1',
            'mi error 2'
        ]

    def tearDown(self):
        super().tearDown()
        # Si existe self.filepath, lo elimina.
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_write_errors(self):
        """Comprueba que guarda los errores."""
        self.payments_utils.write_log_errors(self.errors)
        with open(self.filepath, 'r') as fh:
            data = fh.read()

        self.assertTrue('mi error 1 : mi error 2' in data)
