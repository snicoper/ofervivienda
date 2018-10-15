import os

from gallery import settings as gallery_settings
from tests.unit.images import simple_uploaded_file

from .base_gallery import BaseGalleryTest


class ImageAnuncioTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.image_path = os.path.join(os.path.dirname(__file__), 'image_for_model.jpg')
        self.anuncio = self.anuncio_model.objects.get(pk=1)
        self.image_obj = self.image_model()
        self.image_obj.anuncio = self.anuncio
        self.image_obj.image = simple_uploaded_file(self.image_path)
        self.image_obj.save()

    def tearDown(self):
        super().tearDown()
        if self.image_obj:
            self.image_obj.delete()

    def test_image_obj_creado_con_exito(self):
        """Se ha creado ImageAnuncio."""
        self.assertTrue(self.image_model.objects.get(pk=self.image_obj.pk))

    def test_image_no_requiere_del_campos_description(self):
        """El campo description no es requerido."""
        self.image_obj.description = ''

        # Si no hay error, todo OK.
        self.image_obj.save()

    def test_thumbnail_creado(self):
        """Se ha creado en thumbnail."""
        thumbnail = os.path.join(
            gallery_settings.GALLERY_THUMBNAIL_PATH.format('image_for_model.jpg')
        )

        self.assertEqual(self.image_obj.thumbnail, thumbnail)

    def test_image_resize_anuncio_no_premium(self):
        """Comprueba el tamaño después de subir la imagen."""
        self.assertEqual(self.image_obj.image.width, 600)
        self.assertEqual(self.image_obj.image.height, 375)

    def test_image_resize_anuncio_premium(self):
        """Las dimensiones son mas grandes en un anuncio Premium."""
        self.anuncio.is_premium = True
        self.anuncio.save()
        image_obj = self.image_model()
        image_obj.anuncio = self.anuncio
        image_obj.image = simple_uploaded_file(self.image_path)
        image_obj.save()

        self.assertEqual(image_obj.image.width, 1000)
        self.assertEqual(image_obj.image.height, 625)

        # Eliminar obj para que elimine las imágenes.
        image_obj.delete()

    def test_elimina_las_imagenes_del_disco(self):
        """Cuando se elimina el objeto, también lo hacen las imágenes."""
        image_path = self.image_obj.image.path

        self.assertTrue(os.path.exists(image_path))
        self.image_obj.delete()

        self.assertFalse(os.path.exists(image_path))

        # Poner image_obj en None, para el tearDown
        self.image_obj = None

    def test_cambia_imagen_elimina_la_antigua(self):
        """Cuando se cambia una imagen, se elimina del disco
        la anterior.
        """
        self.image_path = os.path.join(os.path.dirname(__file__), 'image_for_model2.jpg')
        image_path = self.image_obj.image.path
        self.image_obj.image = simple_uploaded_file(self.image_path)
        self.image_obj.save()

        self.assertNotEqual(image_path, self.image_obj.image.path)
        self.assertFalse(os.path.exists(image_path))
