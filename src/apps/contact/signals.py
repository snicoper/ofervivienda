import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import ContactMessage


@receiver(pre_delete, sender=ContactMessage)
def delete_contact_message_handler(sender, instance, **kwargs):
    """Elimina las screenshots físicas antes de eliminar un ContactMessage."""
    if instance.screenshot and os.path.exists(instance.screenshot.path):
        os.remove(instance.screenshot.path)
