from django.conf import settings
from django.db import models

from anuncios.models import Anuncio

from .managers import MessageManager


class Message(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='message_parent',
        null=True,
        blank=True
    )
    anuncio = models.ForeignKey(
        Anuncio,
        on_delete=models.CASCADE,
        related_name='anuncio_thread',
        blank=True,
        null=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_sender'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_recipient'
    )
    body = models.TextField(
        verbose_name='Mensaje'
    )
    subject = models.CharField(
        max_length=255,
        verbose_name='Asunto'
    )
    recipient_read = models.BooleanField(
        default=False
    )
    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    objects = MessageManager()

    class Meta:
        ordering = ('recipient_read', '-sent_at',)
        verbose_name = 'Mensaje privado'
        verbose_name_plural = 'Mensajes privados'

    def __str__(self):
        return self.subject
