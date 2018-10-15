import os
from unittest import TestCase

from PIL import Image

from tests.unit.images import create_image, delete_image, get_image_path
from utils.images import ImageResize


class ImageResizeTest(TestCase):
    """Test redimensionar de imágenes."""

    def setUp(self):
        create_image(size=[300, 150])
        self.media_path = get_image_path
        self.resize_image = ImageResize(self.media_path())

    def tearDown(self):
        delete_image()

    def test_redimensiona_el_width(self):
        """Comprueba que el width es redimensionar a 150."""
        self.resize_image.resize(self.media_path(), 150, 150)

        with Image.open(self.media_path()) as image:
            self.assertEqual(image.size, (150, 75))

    def test_redimensiona_el_height(self):
        """Comprueba que el height es redimensionar a 150."""
        create_image(size=[150, 300])
        self.resize_image.resize(self.media_path(), 150, 150)

        with Image.open(self.media_path()) as image:
            self.assertEqual(image.size, (75, 150))

    def test_redimension_sin_scale(self):
        """Prueba la redimension sin scale."""
        create_image(size=[50, 300])
        self.resize_image.scale = False
        self.resize_image.resize(self.media_path(), 200, 100)

        with Image.open(self.media_path()) as image:
            self.assertEqual(image.size, (200, 100))

    def test_anade_prefix_cuando_es_pasado(self):
        """Cuando se le pasa prefix, se añade al nombre de la imagen."""
        prefix = 'thumbnail_'
        name = '{}test.png'.format(prefix)
        self.resize_image.resize(self.media_path(), 200, 100, prefix=prefix)

        self.assertTrue(os.path.exists(self.media_path(name)))
        delete_image(name)

    def test_raise_filenotfound_exception_cuando_se_le_pasa_una_imagen_que_no_existe(self):
        """Lanza un FileNotFoundError cuando se pasa una imagen que no existe."""
        with self.assertRaises(FileNotFoundError):
            ImageResize('file_not_found.png')
