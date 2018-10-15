from pmessages.models import Message
from tests.unit.base_test import BaseTestCase


class BasePmessagesTest(BaseTestCase):
    """Los fixtures cuenta que perico ha mandado 2 mensajes a snicoper y
    snicoper ha respondido 1 a perico.
    """

    def setUp(self):
        super().setUp()
        self.pmessages_model = Message
        self.anuncio = self.anuncio_model.objects.get(pk=1)
