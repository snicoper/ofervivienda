import sys

from django import forms

from anuncios import models
from utils.text import ucfirst


class SearchAddressForm(forms.Form):
    """Form de búsqueda inline en el home."""
    q = forms.CharField()
    category = forms.ChoiceField(
        choices=models.Anuncio.CATEGORY_CHOICES
    )
    type_anuncio = forms.ChoiceField(
        choices=models.Anuncio.TYPE_ANUNCIO_CHOICES
    )


class BaseSearchForm(forms.ModelForm):
    """Form de búsquedas.

    No instanciar este form NUNCA.
    """
    q = forms.CharField(label='Ubicación')
    category = forms.ChoiceField(
        choices=models.Anuncio.CATEGORY_CHOICES
    )
    type_anuncio = forms.ChoiceField(
        choices=models.Anuncio.TYPE_ANUNCIO_CHOICES
    )

    fields_required = ('q', 'category')

    class Meta:
        localized_fields = ('precio', 'metros_cuadrados')
        exclude = '__all__'
        help_texts = {
            'metros_cuadrados': 'Metros cuadrados mínimo',
            'habitaciones': 'Habitaciones mínimo',
            'banos': 'Baños mínimo',
            'precio': 'Precio máximo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        for field in self.fields:
            if field not in self.fields_required:
                self.fields[field].required = False

    @staticmethod
    def get_form_class(model_name):
        """Obtener una subclase de BaseSearchForm.

        Obtener una instancia con un nombre de CATEGORY_CHOICES.

        Returns:
            Clase en caso de existir, None en caso contrario.
        """
        module = sys.modules[__name__]
        object_model = 'Search{}Form'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)


class BaseViviendaForm(BaseSearchForm):
    """Form para pisos, casas, etc."""

    class Meta(BaseSearchForm.Meta):
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'habitaciones',
            'banos',
            'precio',
            'latitude',
            'longitude',
        )


class SearchPisoForm(BaseViviendaForm):
    """Form para alquiler de pisos."""

    class Meta(BaseViviendaForm.Meta):
        model = models.AnuncioPiso


class SearchCasaForm(BaseViviendaForm):
    """Form para alquiler de casas."""

    class Meta(BaseViviendaForm.Meta):
        model = models.AnuncioCasa


class SearchApartamentoForm(BaseViviendaForm):
    """Form para alquiler de apartamentos."""

    class Meta(BaseViviendaForm.Meta):
        model = models.AnuncioApartamento


class SearchHabitacionForm(BaseSearchForm):
    """Form para alquiler de habitaciones."""

    class Meta(BaseSearchForm.Meta):
        model = models.AnuncioHabitacion
        fields = (
            'category',
            'q',
            'type_anuncio',
            'genero',
            'internet',
            'permite_fumar_habitacion',
            'permite_fumar_piso',
            'precio',
            'latitude',
            'longitude',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_anuncio'].widget = forms.HiddenInput()
        self.initial['type_anuncio'] = models.Anuncio.ALQUILER


class SearchTerrenoForm(BaseSearchForm):
    """Form para terrenos."""

    class Meta(BaseSearchForm.Meta):
        model = models.AnuncioTerreno
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )


class SearchParkingForm(BaseSearchForm):
    """Form para parkings."""

    class Meta(BaseSearchForm.Meta):
        model = models.AnuncioParking
        fields = (
            'category',
            'q',
            'type_anuncio',
            'precio',
            'latitude',
            'longitude',
        )


class SearchIndustrialForm(BaseSearchForm):
    """Form para Naves Industriales."""

    class Meta(BaseSearchForm.Meta):
        model = models.AnuncioIndustrial
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )


class SearchLocalForm(BaseSearchForm):
    """Form para locales."""

    class Meta(BaseSearchForm.Meta):
        model = models.AnuncioLocal
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )
