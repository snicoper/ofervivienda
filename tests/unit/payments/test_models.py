from .base_payments import BasePaymentIpnTest


class PaymentIpnTest(BasePaymentIpnTest):
    """Tests del modelo src/apps/payments/models.py."""

    def setUp(self):
        super().setUp()
        self.user = self.user_model.objects.get(pk=1)

    def test_crear_payment_ipn(self):
        """Crea un objeto."""
        self.create_object('PREMIUM1')
        self.assertEqual(self.payments_model.objects.count(), 1)

    def test_payment_date(self):
        """Se payment_date tiene un valor."""
        ipn = self.create_object('PREMIUM1')
        self.assertTrue(ipn.payment_date)
