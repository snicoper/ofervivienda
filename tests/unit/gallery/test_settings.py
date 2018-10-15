from django.test import TestCase

from gallery import settings as gallery_settings


class GalleerySettingsTest(TestCase):

    def test_settings(self):
        """Prueba los valores de settings en Gallery."""
        self.assertEqual(gallery_settings.GALLERY_IMAGE_WIDTH, 600)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_HEIGHT, 600)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_QUALITY, 60)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_PREMIUM_WIDTH, 1000)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_PREMIUM_HEIGHT, 1000)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_QUALITY_PREMIUM, 90)
        self.assertEqual(gallery_settings.IMAGES_MAX_IMAGES, 5)
        self.assertEqual(gallery_settings.GALLERY_IMAGE_PATH, 'anuncios/')
        self.assertEqual(gallery_settings.GALLERY_THUMBNAIL_WIDTH, 300)
        self.assertEqual(gallery_settings.GALLERY_THUMBNAIL_HEIGHT, 200)
        self.assertEqual(gallery_settings.GALLERY_THUMBNAIL_PATH, 'anuncios/thumbnail_{}')
        self.assertEqual(gallery_settings.GALLERY_THUMBNAIL_DEFAULT, 'dummy-image.jpg')
