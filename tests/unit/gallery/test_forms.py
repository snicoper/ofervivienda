import os

from gallery.forms import ImageAnuncioCreateForm, ImageAnuncioForm
from tests.unit.images import simple_uploaded_file

from .base_gallery import BaseGalleryTest


class ImageAnuncioFormTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        self.form = ImageAnuncioForm(
            {'anuncio': '1'},
            {'image': simple_uploaded_file(self.image_path)},
            {'description': ''}
        )

    def test_form_valid(self):
        """Form valido."""
        self.assertTrue(self.form.is_valid())


class ImageAnuncioCreateFormTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        self.form = ImageAnuncioCreateForm(
            {'anuncio': ''},
            {'image': None},
            {'description': ''}
        )

    def test_form_valid(self):
        """Form valido, no requiere ningún campo, es la vista quien se encarga."""
        self.assertTrue(self.form.is_valid())
