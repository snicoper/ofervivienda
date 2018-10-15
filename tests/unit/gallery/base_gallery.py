from gallery.models import ImageAnuncio
from tests.unit.base_test import BaseTestCase


class BaseGalleryTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.image_model = ImageAnuncio
