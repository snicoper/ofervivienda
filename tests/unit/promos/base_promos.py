from promos.models import Promo
from tests.unit.base_test import BaseTestCase


class BasePromoTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.promo_model = Promo
