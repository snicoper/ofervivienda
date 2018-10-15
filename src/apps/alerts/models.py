import sys

from django.conf import settings
from django.db import models
from django.urls import reverse

from anuncios.mixins import models as model_mixins
from anuncios.models import AbstractAnuncioModel
from localization.models import AbstractLocationModel
from utils.text import ucfirst


class AbstractAlertModel(AbstractAnuncioModel):

    class Meta:
        abstract = True


class AlertAnuncio(AbstractLocationModel, AbstractAlertModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Autor',
        related_name='alerts_owner'
    )
    description = models.CharField(
        max_length=255
    )

    class Meta:
        unique_together = (('owner', 'description'),)

    def __str__(self):
        return self.owner.username

    def get_absolute_url(self):
        return reverse('alerts:details', kwargs={'pk': self.pk})

    @staticmethod
    def get_model_class(model_name):
        """Obtener una subclase de AlertAnuncio.

        Obtener una instancia con un nombre de CATEGORY_CHOICES.

        Returns:
            Clase en caso de existir, None en caso contrario.
        """
        module = sys.modules[__name__]
        object_model = 'Alert{}'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)


class AlertPiso(model_mixins.AnuncioPisoMixin, AlertAnuncio):
    pass


class AlertCasa(model_mixins.AnuncioCasaMixin, AlertAnuncio):
    pass


class AlertApartamento(model_mixins.AnuncioApartamentoMixin, AlertAnuncio):
    pass


class AlertHabitacion(model_mixins.AnuncioHabitacionMixin, AlertAnuncio):
    pass


class AlertTerreno(model_mixins.AnuncioTerrenoMixin, AlertAnuncio):
    pass


class AlertParking(model_mixins.AnuncioParkingMixin, AlertAnuncio):
    pass


class AlertIndustrial(model_mixins.AnuncioIndustrialMixin, AlertAnuncio):
    pass


class AlertLocal(model_mixins.AnuncioLocalMixin, AlertAnuncio):
    pass
