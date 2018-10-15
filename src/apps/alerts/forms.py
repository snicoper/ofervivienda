import sys

from django import forms

from anuncios.models import Anuncio
from utils.text import ucfirst

from . import models


class BaseAlertForm(forms.ModelForm):
    category = forms.ChoiceField(choices=Anuncio.CATEGORY_CHOICES)

    class Meta:
        localized_fields = ('precio', 'metros_cuadrados')
        help_texts = {
            'metros_cuadrados': 'Metros cuadrados mínimo',
            'habitaciones': 'Mínimo de habitaciones',
            'banos': 'Mínimo de baños',
            'precio': 'Precio máximo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['owner', 'polygon', 'latitude', 'longitude']
        required_fields = ['category', 'owner', 'polygon', 'latitude', 'longitude', 'description']
        for field in self.fields:
            if field not in required_fields:
                self.fields[field].required = False
            else:
                self.fields[field].required = True
            if field in hidden_fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        """Polygon esta oculto y hay que informar si se deja en blanco.

        Al ser un campo oculto, cuando no se marca zona el error no
        se muestra. De esta manera, el usuario podrá saber que pasa.
        """
        cleaned_data = super().clean()
        polygon = cleaned_data.get('polygon')
        if not polygon:
            # Override errores del campo polygon.
            self._errors['polygon'] = ''
            raise forms.ValidationError('Has de marcar una zona en el mapa!')
        return cleaned_data

    def clean_description(self):
        """Personalizar la alerta de descripción."""
        description = self.cleaned_data['description']
        if not self.instance.pk:
            owner = self.data.get('owner')
            if models.AlertAnuncio.objects.filter(owner=owner, description=description):
                raise forms.ValidationError('Ya tienes una alerta con esa descripción')
        return description

    def clean_polygon(self):
        polygon = self.cleaned_data['polygon']
        return polygon

    @staticmethod
    def get_form_class(model_name):
        """Obtener una subclase de BaseAlertForm.

        Obtener una instancia con un nombre de CATEGORY_CHOICES.

        Returns:
            Clase en caso de existir, None en caso contrario.
        """
        module = sys.modules[__name__]
        object_model = 'Alert{}Form'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)


class BaseViviendaForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'estado_inmueble',
            'metros_cuadrados',
            'habitaciones',
            'banos',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]


class AlertPisoForm(BaseViviendaForm):

    class Meta(BaseViviendaForm.Meta):
        model = models.AlertPiso


class AlertCasaForm(BaseViviendaForm):

    class Meta(BaseViviendaForm.Meta):
        model = models.AlertCasa


class AlertApartamentoForm(BaseViviendaForm):

    class Meta(BaseViviendaForm.Meta):
        model = models.AlertApartamento


class AlertHabitacionForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        model = models.AlertHabitacion
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'genero',
            'internet',
            'permite_fumar_piso',
            'permite_fumar_habitacion',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_anuncio'].widget = forms.HiddenInput()
        self.initial['type_anuncio'] = models.AlertAnuncio.ALQUILER


class AlertTerrenoForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        model = models.AlertTerreno
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]


class AlertParkingForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        model = models.AlertParking
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]


class AlertIndustrialForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        model = models.AlertIndustrial
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]


class AlertLocalForm(BaseAlertForm):

    class Meta(BaseAlertForm.Meta):
        model = models.AlertLocal
        fields = [
            'owner',
            'description',
            'category',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
            'polygon',
        ]
