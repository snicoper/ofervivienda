import sys
from random import randint

from django.conf import settings
from django.db import models
from django.urls import reverse

from gallery import settings as gallery_settings
from localization.models import AbstractLocationModel
from utils.text import ucfirst

from .managers import AnuncioManager
from .mixins import models as model_mixins
from .utils import notify_precio_anuncio_baja


class AbstractAnuncioModel(models.Model):
    """Modelo abstracto para Anuncios."""
    ####################################
    # Categorías.
    ####################################
    PISO = 'PISO'
    CASA = 'CASA'
    APARTAMENTO = 'APARTAMENTO'
    HABITACION = 'HABITACION'
    TERRENO = 'TERRENO'
    PARKING = 'PARKING'
    INDUSTRIAL = 'INDUSTRIAL'
    LOCAL = 'LOCAL'

    CATEGORY_CHOICES = (
        (PISO, 'Piso'),
        (CASA, 'Casa'),
        (APARTAMENTO, 'Apartamento'),
        (HABITACION, 'Habitacion'),
        (TERRENO, 'Terreno'),
        (PARKING, 'Parking'),
        (INDUSTRIAL, 'Nave Industrial'),
        (LOCAL, 'Local'),
    )

    ####################################
    # Tipo de anuncio.
    ####################################

    VENTA = 'VENTA'
    ALQUILER = 'ALQUILER'

    TYPE_ANUNCIO_CHOICES = (
        (VENTA, 'Venta'),
        (ALQUILER, 'Alquiler'),
    )

    ####################################
    # Estado del inmueble.
    ####################################

    OBRANUEVA = 'OBRANUEVA'
    BUENESTADO = 'BUENESTADO'
    AREFORMAR = 'AREFORMAR'

    ESTADO_INMUEBLE_CHOICES = (
        (OBRANUEVA, 'Obra nueva'),
        (BUENESTADO, 'Buen estado'),
        (AREFORMAR, 'A reformar')
    )

    ####################################
    # Monedas.
    ####################################

    EUR = 'EUR'
    USD = 'USD'
    GBP = 'GBP'

    CURRENCY_SYMBOLS = (
        ('EUR', '€'),
        ('USD', '$'),
        ('GBP', '£'),
    )

    category = models.CharField(
        verbose_name='Categoría',
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    type_anuncio = models.CharField(
        verbose_name='Tipo anuncio',
        max_length=50,
        choices=TYPE_ANUNCIO_CHOICES
    )
    estado_inmueble = models.CharField(
        verbose_name='Estado',
        max_length=50,
        choices=ESTADO_INMUEBLE_CHOICES,
        default='',
        blank=True
    )
    metros_cuadrados = models.PositiveIntegerField(
        verbose_name='Metros cuadrados',
        blank=True,
        null=True
    )
    precio = models.DecimalField(
        verbose_name='Precio',
        max_digits=7,
        decimal_places=0,
        blank=True,
        null=True
    )
    currency = models.CharField(
        verbose_name='Moneda',
        choices=CURRENCY_SYMBOLS,
        max_length=3,
        default=EUR
    )
    active = models.BooleanField(
        verbose_name='Activo',
        default=True
    )
    create_at = models.DateTimeField(
        verbose_name='Fecha creación',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name='Fecha ultima modificación',
        auto_now=True
    )

    class Meta:
        abstract = True


class Anuncio(AbstractLocationModel, AbstractAnuncioModel):
    """Modelo de anuncios.

    Sobre escribe update_at ya que se ha de cambiar explícitamente.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='owner',
        related_name='anuncios_owner'
    )
    is_premium = models.BooleanField(
        verbose_name='Anuncio premium',
        default=False
    )
    phone = models.CharField(
        verbose_name='Teléfono contacto',
        max_length=20,
        blank=True,
        default=''
    )
    description = models.TextField(
        verbose_name='Descripción',
        blank=True,
        default=''
    )
    views = models.IntegerField(
        verbose_name='Visitas',
        blank=True,
        default=0,
    )
    update_at = models.DateTimeField(
        verbose_name='Fecha ultima modificación',
        auto_now_add=True
    )

    objects = AnuncioManager()

    class Meta:
        ordering = ('-active', '-is_premium', '-update_at')

    def __init__(self, *args, **kwargs):
        """Guardar el precio para ver si cambia en caso de hacer cambios en el
        campo self.precio.
        """
        super().__init__(*args, **kwargs)
        self._original_precio = self.precio

    def __str__(self):
        return self.get_title

    def save(self, *args, **kwargs):
        """Si ha bajado el precio, notificar por email a los usuarios que lo
        tienen en favoritos.
        """
        if self.pk:
            if self.precio < self._original_precio:
                notify_precio_anuncio_baja(self, self._original_precio)
        super().save(*args, **kwargs)
        self._original_precio = self.precio

    def get_absolute_url(self):
        return reverse('anuncios:details', kwargs={'pk': self.pk})

    @property
    def get_title(self):
        """Genera un titulo con la category, type_anuncio y location_string."""
        return '{} en {}: {}'.format(
            self.get_category_display(),
            self.get_type_anuncio_display(),
            self.location_string
        )

    @property
    def get_random_thumbnail(self):
        """Obtener un thumbnail aleatorio de las imágenes asociadas.

        Añade en la devolución el {{ MEDIA_URL }}.

        Example:
            <img src="{{ anuncio.get_random_thumbnail }}">

        Returns:
            str: Un thumbnail aleatorio en caso de tener imágenes, en caso
            contrario, devolverá la imagen por defecto.
        """
        media_url = settings.MEDIA_URL + '{}'
        images = self.image_anuncio.all()
        if images:
            return media_url.format(images[randint(0, len(images) - 1)].thumbnail)
        else:
            return media_url.format(gallery_settings.GALLERY_THUMBNAIL_DEFAULT)

    @property
    def get_ratio(self):
        """Obtener el ratio del anuncio.

        Returns:
            float|int: Ratio medio del anuncio 0 en caso de no tener ratio.
        """
        # ratio_anuncio es related_name (src/apps/ratings/models.py)
        ratio = self.ratio_anuncio.aggregate(models.Avg('score'))
        if ratio['score__avg']:
            return ratio['score__avg']
        return 0

    @staticmethod
    def get_model_class(model_name):
        """Obtener una subclase de Anuncio.

        Obtener una instancia con un nombre de CATEGORY_CHOICES.

        Returns:
            Clase en caso de existir, None en caso contrario.
        """
        module = sys.modules[__name__]
        object_model = 'Anuncio{}'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)


class AnuncioPiso(model_mixins.AnuncioPisoMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioCasa(model_mixins.AnuncioCasaMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioApartamento(model_mixins.AnuncioApartamentoMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioHabitacion(model_mixins.AnuncioHabitacionMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioTerreno(model_mixins.AnuncioTerrenoMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioParking(model_mixins.AnuncioParkingMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioIndustrial(model_mixins.AnuncioIndustrialMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True


class AnuncioLocal(model_mixins.AnuncioLocalMixin, Anuncio):

    class Meta:
        manager_inheritance_from_future = True
