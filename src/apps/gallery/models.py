import os

from django.conf import settings
from django.db import models

from anuncios.models import Anuncio
from utils.images import ImageResize

from . import settings as images_settings


class ImageAnuncio(models.Model):
    """Imagen de un anuncio."""
    anuncio = models.ForeignKey(
        Anuncio,
        on_delete=models.CASCADE,
        verbose_name='Anuncio',
        related_name='image_anuncio',
    )
    image = models.ImageField(
        verbose_name='Imagen',
        upload_to=images_settings.GALLERY_IMAGE_PATH
    )
    thumbnail = models.CharField(
        verbose_name='Thumbnail',
        max_length=100,
        blank=True
    )
    description = models.CharField(
        verbose_name='Descripción',
        max_length=100,
        default='',
        blank=True
    )

    def __str__(self):
        """ID de la imagen para mostrarla en admin Anuncio."""
        return str(self.id)

    def save(self, *args, **kwargs):
        """Genera el nombre de thumbnail y elimina si se cambia.

        Si la imagen se ha cambiado, la antigua sera eliminada del disco, también
        genera el nombre para el thumbnail.

        Una imagen .png la convertirá a .jpeg para poderle aplicar los filtros,
        de lo contrario las imágenes .png pueden llegar a pasar mucho.

        Renombrar la extensión de .png a .jpg antes de manipular la imagen.

        Se ha de indicar en ImageResize.png2jpeg = True.
        """
        if not self.id:
            if self.image.name[-4:].lower() == '.png':
                self.image.name = '{}{}'.format(self.image.name[:-4], '.jpg')
        else:
            old_image = ImageAnuncio.objects.get(pk=self.id)
            old_image_path = old_image.image.path
            old_thumbnail_name = old_image.thumbnail
            if old_image_path != self.image.path:
                self._remove_old_images(old_image_path, old_thumbnail_name)
        # Es necesario guardar antes de asignar el nombre al thumbnail para
        # que luego el nombre sea el mismo.
        super().save(*args, **kwargs)
        self.thumbnail = images_settings.GALLERY_THUMBNAIL_PATH.format(
            os.path.basename(self.image.name)
        )
        super().save(*args, **kwargs)
        self._resize_images(png2jpeg=True)

    def _remove_old_images(self, old_image_path, old_thumbnail_name):
        """Elimina imagen y thumbnail del disco.

        Args:
            old_image_path (str): Path absoluto de la imagen.
            old_thumbnail_name (str): Nombre de la imagen (upload_to).
        """
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, old_thumbnail_name)
        if os.path.exists(thumbnail_path) and os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
        if os.path.exists(old_image_path) and os.path.isfile(old_image_path):
            os.remove(old_image_path)

    def _resize_images(self, png2jpeg=False):
        """Redimensionar image y thumbnail.

        El thumbnail no escalar, desajusta el diseño en las cards.

        Args:
            png2jpeg: Convertir png a jpeg?
        """
        if self.anuncio.is_premium:
            width = images_settings.GALLERY_IMAGE_PREMIUM_WIDTH
            height = images_settings.GALLERY_IMAGE_PREMIUM_HEIGHT
            quality = images_settings.GALLERY_IMAGE_QUALITY_PREMIUM
        else:
            width = images_settings.GALLERY_IMAGE_WIDTH
            height = images_settings.GALLERY_IMAGE_WIDTH
            quality = images_settings.GALLERY_IMAGE_QUALITY
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, self.thumbnail)
        thumbnail_width = images_settings.GALLERY_THUMBNAIL_WIDTH
        thumbnail_height = images_settings.GALLERY_THUMBNAIL_HEIGHT
        img = ImageResize(self.image.path)
        img.png2jpeg = True
        img.quality = quality
        img.resize(self.image.path, width, height)
        img.scale = False
        img.resize(thumbnail_path, thumbnail_width, thumbnail_height)
