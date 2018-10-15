from django.db import models


class AnuncioViviendaMixin(models.Model):
    """Propiedades exclusivos para las viviendas."""
    habitaciones = models.PositiveSmallIntegerField(
        verbose_name='Habitaciones'
    )
    banos = models.PositiveSmallIntegerField(
        verbose_name='Baños'
    )
    ano_construccion = models.PositiveSmallIntegerField(
        verbose_name='Año de construcción',
        blank=True,
        null=True
    )
    parking = models.BooleanField(
        verbose_name='Plaza Parking',
        default=False,
        blank=True
    )

    class Meta:
        abstract = True


class AnuncioPisoMixin(AnuncioViviendaMixin):
    """Propiedades exclusivos para Piso."""

    class Meta:
        abstract = True


class AnuncioCasaMixin(AnuncioViviendaMixin):
    """Propiedades exclusivos para Casa."""

    class Meta:
        abstract = True


class AnuncioApartamentoMixin(AnuncioViviendaMixin):
    """Propiedades exclusivos para Apartamento."""

    class Meta:
        abstract = True


class AnuncioHabitacionMixin(models.Model):
    """Propiedades exclusivos para Habitacion."""
    CHICOCHICA = 'CHICOCHICA'
    CHICO = 'CHICO'
    CHICA = 'CHICA'
    GENERO_CHOICES = (
        (CHICOCHICA, 'Chicos y Chicas'),
        (CHICO, 'Chicos'),
        (CHICA, 'Chicas'),
    )

    permite_fumar_habitacion = models.BooleanField(
        verbose_name='Fumar en habitación',
        default=False,
        blank=True
    )
    permite_fumar_piso = models.BooleanField(
        verbose_name='Fumar en el piso',
        default=False,
        blank=True
    )
    internet = models.BooleanField(
        verbose_name='Conexión a Internet',
        default=False,
        blank=True
    )
    genero = models.CharField(
        verbose_name='Genero',
        max_length=20,
        choices=GENERO_CHOICES,
        default=CHICOCHICA
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Las habitaciones siempre son ALQUILER."""
        if not self.pk:
            self.type_anuncio = self.ALQUILER
        super().save(*args, **kwargs)


class AnuncioTerrenoMixin(models.Model):
    """Propiedades exclusivos para Terreno."""

    class Meta:
        abstract = True


class AnuncioParkingMixin(models.Model):
    """Propiedades exclusivos para Parking."""

    class Meta:
        abstract = True


class AnuncioIndustrialMixin(models.Model):
    """Propiedades exclusivos para Industrial."""

    class Meta:
        abstract = True


class AnuncioLocalMixin(models.Model):
    """Propiedades exclusivos para Local."""

    class Meta:
        abstract = True
