from django.db import models


class ContactMessage(models.Model):
    """Mensajes enviados desde el formulario de contacto."""
    subject = models.CharField(
        verbose_name='Asunto',
        max_length=255,
    )
    message = models.TextField(
        verbose_name='Mensaje'
    )
    username = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    screenshot = models.ImageField(
        verbose_name='Imagen',
        upload_to='contact/screenshots',
        blank=True,
        default=''
    )
    read = models.BooleanField(
        verbose_name='Leído',
        default=False
    )
    is_register = models.BooleanField(
        verbose_name='Usuario registrado'
    )
    create_at = models.DateTimeField(
        verbose_name='Fecha creación',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Mensaje contacto'
        verbose_name_plural = 'Mensajes contacto'
        ordering = ('read', '-create_at')
        permissions = (
            ('can_view_messages', 'Puede ver mensaje contacto'),
        )

    def __str__(self):
        return self.subject
