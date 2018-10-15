import os

from payments import settings as payments_settings, utils as payments_utils
from payments.models import PaymentIpn
from tests.unit.base_test import BaseTestCase


class BasePaymentIpnTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.data_json = None
        self.payments_model = PaymentIpn
        self.payments_settings = payments_settings
        self.payments_utils = payments_utils
        self.choices = {k: v for k, v in PaymentIpn.PAYMENT_CHOICES}
        filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.json')
        self.data_json = self.load_data(filepath)

    def create_object(self, key):
        """Crea un objeto con los datos de data.json.

        Args:
            key (str): Una de las keys en data.json

        Returns:
            Un objeto PaymentIpn.
        """
        data = self.data_json[key]
        return self.payments_model.objects.create(
            user=self.user,
            item_name=data['item_name'],
            item_number=data['item_number'],
            invoice=data['invoice'],
            txn_id=data['txn_id'],
            payment_status=data['payment_status'],
            total_amount=data['mc_gross'],
            receiver_amount=float(data['mc_gross']) - float(data['mc_fee']),
            post_data=data
        )
