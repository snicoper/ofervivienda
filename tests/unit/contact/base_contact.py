from contact.models import ContactMessage
from tests.unit.base_test import BaseTestCase


class BaseContactTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.contact_model = ContactMessage
