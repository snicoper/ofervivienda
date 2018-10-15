from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from dateutil import relativedelta

from localization.models import AbstractLocationModel
from utils.images import ImageResize
from utils.mixins.models import ImageUpdateModel

from . import settings as accounts_settings


class User(ImageUpdateModel, AbstractUser):
    """Perfil de usuario."""
    slug = models.SlugField(
        max_length=150,
        blank=True
    )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to=accounts_settings.ACCOUNTS_AVATAR_PATH,
        default='',
        blank=True
    )
    public_name = models.CharField(
        verbose_name='Nombre a mostrar',
        max_length=50,
        default='',
        blank=True
    )
    phone = models.CharField(
        verbose_name='Teléfono',
        max_length=30,
        blank=True,
        default=''
    )
    description = models.TextField(
        verbose_name='Descripción',
        blank=True,
        default=''
    )
    is_premium = models.BooleanField(
        verbose_name='¿Es cuenta Premium?',
        default=False
    )
    anuncios_premium = models.IntegerField(
        verbose_name='Numero de anuncios Premium',
        default=0
    )
    expire_premium_at = models.DateTimeField(
        verbose_name='Fecha de expiración cuenta Premium',
        blank=True
    )

    _image_fields = ['avatar']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_avatar = None

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """Comprueba si ha añadido o cambiado el avatar.

        Si acaba de crear la cuenta, se pondrá en self.expire_premium_at
        a un día anterior a now().
        """
        self.slug = slugify(self.username)
        if not self.pk:
            self.expire_premium_at = timezone.now() - timezone.timedelta(days=1)
        if self.avatar and self.old_avatar != self.avatar:
            super().save(*args, **kwargs)
            image_resize = ImageResize(self.avatar.path)
            image_resize.resize(
                save_path=self.avatar.path,
                width=accounts_settings.ACCOUNTS_AVATAR_WIDTH,
                height=accounts_settings.ACCOUNTS_AVATAR_HEIGHT
            )
            self.old_avatar = self.avatar
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Obtener el URLConf para el perfil privado."""
        return reverse('accounts:profile')

    @property
    def get_avatar(self):
        """Obtener avatar usuario.

        Al usar get_avatar no requiere de {{ MEDIA_URL }}.

        Returns:
            str: Avatar del usuario o imagen por defecto.

            Si el usuario tiene un avatar, obtendrá el del usuario, en caso
            contrario, el avatar por defecto.
        """
        if not self.avatar or not self.avatar.path:
            return '{}{}/{}'.format(
                settings.MEDIA_URL,
                accounts_settings.ACCOUNTS_AVATAR_PATH,
                accounts_settings.ACCOUNTS_AVATAR_DEFAULT
            )
        return '{}/{}'.format(settings.MEDIA_URL, self.avatar)

    @property
    def get_public_name(self):
        """Obtiene el nombre público.

        Depende de si lo tiene puesto o no, si lo tiene puesto lo devolverá, en
        caso contrario, devolverá el username.
        """
        return self.public_name if self.public_name else self.username

    def update_premium(self, months):
        """Actualiza la cuenta Premium.

        Si Premium no esta activo o esta expirado, pondrá expire_premium_at a
        now(), en caso contrario, si esta activa y con tiempo, se le incrementara
        el tiempo de expiración mas los months.

        Args:
            months (int): Meses a incrementar.
        """
        if not self.is_premium:
            self.is_premium = True
        if self.expire_premium_at < timezone.now():
            self.expire_premium_at = timezone.now()
        self.expire_premium_at += relativedelta.relativedelta(months=months)

    def increase_anuncio(self):
        """Incrementa en 1 el numero de anuncios_premium."""
        self.anuncios_premium += 1

    def decrease_anuncio(self):
        """Decrementar en 1 el numero de anuncios_premium."""
        if self.anuncios_premium > 0:
            self.anuncios_premium -= 1


class UserOptions(models.Model):
    """Opciones de usuario."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Opciones de usuario',
        related_name='user_options'
    )
    phone_public = models.BooleanField(
        verbose_name='Teléfono público',
        default=False
    )
    address_public = models.BooleanField(
        verbose_name='Dirección publica',
        default=False
    )
    email_public = models.BooleanField(
        verbose_name='Email público',
        default=False
    )
    notify_precio_anuncio_baja = models.BooleanField(
        verbose_name='Notificar si el precio baja',
        default=True
    )

    class Meta:
        verbose_name = 'Opciones de usuario'
        verbose_name_plural = 'Opciones de usuarios'

    def __str__(self):
        return self.user.username


class UserLocation(AbstractLocationModel):
    """Localización del usuario."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Localización usuario',
        related_name='user_location'
    )

    class Meta:
        verbose_name = 'Localización de usuario'
        verbose_name_plural = 'Localizaciones de usuarios'

    def __str__(self):
        return self.user.username
