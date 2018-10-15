from payments.forms import PaypalIpnForm

from .base_payments import BasePaymentIpnTest


class PaypalIpnFormTest(BasePaymentIpnTest):
    """Form src/apps/payments/forms.py."""

    def test_campo_return_existe(self):
        """Comprueba que el campo return existe en el form."""
        form = PaypalIpnForm()
        self.assertTrue(form['return'])
