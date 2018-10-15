from accounts import settings as accounts_settings
from tests.unit.base_test import BaseTestCase


class BaseAccountsTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.accounts_settings = accounts_settings
