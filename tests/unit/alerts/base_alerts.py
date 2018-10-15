import os

from tests.unit.base_test import BaseTestCase


class BaseTestAlerts(BaseTestCase):

    def setUp(self):
        super().setUp()
        json_file = os.path.join(os.path.dirname(__file__), 'form_data.json')
        self.form_data = self.load_data(json_file)
