import os

from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import ImageAnuncio


@receiver(pre_delete, sender=ImageAnuncio)
def anuncioimage_pre_delete_handler(sender, instance, using, **kwargs):
    """Elimina la imagen y el thumbnail en disco."""
    image_path = instance.image.path
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, instance.thumbnail)
    if os.path.exists(image_path) and os.path.isfile(image_path):
        os.remove(image_path)
    if os.path.exists(thumbnail_path) and os.path.isfile(thumbnail_path):
        os.remove(thumbnail_path)
