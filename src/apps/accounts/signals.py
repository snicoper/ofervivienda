import os

from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from favorites.models import Favorites

from .models import UserLocation, UserOptions


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_handler(sender, instance, created, **kwargs):
    """Signal después de crear un usuario.

    Crea Favorites, UserLocation y UserOptions asociados al usuario.
    """
    if created:
        Favorites.objects.create(owner=instance)
        UserLocation.objects.create(user=instance)
        UserOptions.objects.create(user=instance)


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_handler(sender, instance, **kwargs):
    """Elimina el avatar del directorio."""
    if instance.avatar and os.path.exists(instance.avatar.path):
        os.remove(instance.avatar.path)
