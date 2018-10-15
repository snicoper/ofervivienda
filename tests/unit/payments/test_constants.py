from payments.models import PaymentIpn

from .base_payments import BasePaymentIpnTest


class SettingsTest(BasePaymentIpnTest):
    """Tests src/apps/payments/settings.py."""

    def setUp(self):
        super().setUp()
        self.choices_reverse = {v: k for k, v in PaymentIpn.PAYMENT_CHOICES}

    def test_default_constants_settings(self):
        """Comprueba las constantes de settings."""
        self.assertEqual(self.payments_settings.PAYMENTS_PREMIUM1, 7.00)
        self.assertEqual(self.payments_settings.PAYMENTS_PREMIUM3, 19.95)
        self.assertEqual(self.payments_settings.PAYMENTS_PREMIUM6, 38.64)
        self.assertEqual(self.payments_settings.PAYMENTS_PREMIUM12, 73.92)
        self.assertEqual(self.payments_settings.PAYMENTS_ANUNCIO, 2.00)

    def test_choices(self):
        """Comprueba las choices del modelo."""
        # Probar keys
        self.assertEqual(self.choices_reverse.get('1 Mes Premium'), 'PREMIUM1')
        self.assertEqual(self.choices_reverse.get('3 Meses Premium'), 'PREMIUM3')
        self.assertEqual(self.choices_reverse.get('6 Meses Premium'), 'PREMIUM6')
        self.assertEqual(self.choices_reverse.get('1 Año Premium'), 'PREMIUM12')
        self.assertEqual(self.choices_reverse.get('Anuncio Premium'), 'ANUNCIO')

        # Probar Valores
        self.assertEqual(self.choices.get('PREMIUM1'), '1 Mes Premium')
        self.assertEqual(self.choices.get('PREMIUM3'), '3 Meses Premium')
        self.assertEqual(self.choices.get('PREMIUM6'), '6 Meses Premium')
        self.assertEqual(self.choices.get('PREMIUM12'), '1 Año Premium')
        self.assertEqual(self.choices.get('ANUNCIO'), 'Anuncio Premium')

    def test_veriables_config_settings(self):
        """Prueba el valor de config.settings."""
        from config.settings import local
        from config.settings import prod
        from config.settings import test

        # PAYPAL_FORM_ACTION
        self.assertEqual(local.PAYPAL_FORM_ACTION, 'https://www.sandbox.paypal.com/cgi-bin/webscr')
        self.assertEqual(prod.PAYPAL_FORM_ACTION, 'https://www.paypal.com/cgi-bin/webscr')
        self.assertEqual(test.PAYPAL_FORM_ACTION, 'http://127.0.0.1:5000/')

        # PAYPAL_RECEIVER_EMAIL
        self.assertEqual(local.PAYPAL_RECEIVER_EMAIL, 'snicoper-facilitator@gmail.com')
        self.assertEqual(prod.PAYPAL_RECEIVER_EMAIL, 'snicoper@ofervivienda.com')
        self.assertEqual(test.PAYPAL_RECEIVER_EMAIL, 'snicoper-facilitator@gmail.com')
