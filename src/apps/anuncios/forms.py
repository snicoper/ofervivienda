import sys

from django import forms

from utils.text import ucfirst

from . import models


class BaseAnuncioForm(forms.ModelForm):
    """Formulario base para crear y actualizar anuncios.

    Este Form no se instancia directamente NUNCA.

    type_anuncio es relativo, por eso esta en campos no requeridos.
    @ver: BaseAnuncioViviendaForm.clean_estado_inmueble

    Las subclases que se creen, el nombre ha de ser AnuncioXxxxxForm, donde
    Xxxxx la categoría del anuncio.

    @ver: self.get_form_class()
    """
    fields_not_required = [
        'ano_construccion',
        'estado_inmueble',
        'description',
        'parking',
        'phone',
        'is_premium',
        'permite_fumar_piso',
        'permite_fumar_habitacion',
        'internet',
    ]
    fields_hidden = ['owner', 'category', 'is_premium', 'latitude', 'longitude']

    class Meta:
        localized_fields = ('precio', 'metros_cuadrados', 'ano_construccion')
        exclude = '__all__'
        help_texts = {
            'address': 'Si quieres mantener la privacidad, pon solo la calle.',
            'phone': 'Si no se añade, solo se podrá contactar por mensaje privado.',
            'description': 'Cualquier descripción que quieras aportar.',
            'genero': '¿Buscas un genero concreto?',
            'permite_fumar_piso': '¿Se permite fumar en la vivienda?',
            'permite_fumar_habitacion': '¿Se permite fumar en la habitación?'
        }

    def __init__(self, *args, **kwargs):
        """Recorre los campos del form y los añade como required, etc.

        Utiliza las propiedades:
            - fields_not_required: Campos que no serán obligatorios.
            - fields_hidden: Campos que serán ocultos.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in self.fields_not_required:
                self.fields[field].required = False
            else:
                self.fields[field].required = True
            if field in self.fields_hidden:
                self.fields[field].widget = forms.HiddenInput()

    def clean_precio(self):
        """El precio ha de ser mayor de 0."""
        precio = self.cleaned_data['precio']
        if precio <= 0:
            msg_error = 'El precio ha de ser mayor a 0'
            raise forms.ValidationError(msg_error)
        return precio

    def clean_metros_cuadrados(self):
        """Metros cuadrados ha de ser mayor de 0."""
        metros_cuadrados = self.cleaned_data['metros_cuadrados']
        if metros_cuadrados <= 0:
            msg_error = 'Metros cuadrados ha de ser mayor a 0'
            raise forms.ValidationError(msg_error)
        return metros_cuadrados

    @staticmethod
    def get_form_class(model_name):
        """Obtener una subclase de BaseAnuncioForm.

        Obtener una instancia con un nombre de CATEGORY_CHOICES.

        Returns:
            Clase en caso de existir, None en caso contrario.
        """
        module = sys.modules[__name__]
        object_model = 'Anuncio{}Form'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)


class BaseAnuncioViviendaForm(BaseAnuncioForm):
    """Form vivienda base, para piso, casa y apartamento."""

    class Meta(BaseAnuncioForm.Meta):
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'type_anuncio',
            'estado_inmueble',
            'metros_cuadrados',
            'habitaciones',
            'banos',
            'ano_construccion',
            'parking',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )

    def clean_estado_inmueble(self):
        """Comprueba el valor de type_anuncio.

        Si type_anuncio es 'VENTA', el campo estado_inmueble sera requerido y
        lanzara ValidationError, en caso contrario, estado_inmueble no sera requerido.
        """
        estado_inmueble = self.cleaned_data['estado_inmueble']
        type_anuncio = self.data.get('type_anuncio', None)
        if type_anuncio == models.Anuncio.VENTA:
            if not estado_inmueble:
                msg_error = 'Este campo es obligatorio.'
                raise forms.ValidationError(msg_error)
        return estado_inmueble

    def clean_habitaciones(self):
        habitaciones = self.cleaned_data['habitaciones']
        if habitaciones <= 0:
            msg_error = 'El numero de habitaciones ha de ser mayor a 0'
            raise forms.ValidationError(msg_error)
        return habitaciones

    def clean_banos(self):
        banos = self.cleaned_data['banos']
        if banos <= 0:
            msg_error = 'El numero de baños ha de ser mayor a 0'
            raise forms.ValidationError(msg_error)
        return banos


class AnuncioPisoForm(BaseAnuncioViviendaForm):

    class Meta(BaseAnuncioViviendaForm.Meta):
        model = models.AnuncioPiso


class AnuncioCasaForm(BaseAnuncioViviendaForm):

    class Meta(BaseAnuncioViviendaForm.Meta):
        model = models.AnuncioCasa


class AnuncioApartamentoForm(BaseAnuncioViviendaForm):

    class Meta(BaseAnuncioViviendaForm.Meta):
        model = models.AnuncioApartamento


class AnuncioHabitacionForm(BaseAnuncioForm):

    class Meta(BaseAnuncioForm.Meta):
        model = models.AnuncioHabitacion
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'genero',
            'phone',
            'type_anuncio',
            'permite_fumar_piso',
            'permite_fumar_habitacion',
            'internet',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_anuncio'].widget = forms.HiddenInput()
        self.initial['type_anuncio'] = models.Anuncio.ALQUILER


class AnuncioTerrenoForm(BaseAnuncioForm):

    class Meta(BaseAnuncioForm.Meta):
        model = models.AnuncioTerreno
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'metros_cuadrados',
            'type_anuncio',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )


class AnuncioParkingForm(BaseAnuncioForm):

    class Meta(BaseAnuncioForm.Meta):
        model = models.AnuncioParking
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'type_anuncio',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )


class AnuncioIndustrialForm(BaseAnuncioForm):

    class Meta(BaseAnuncioForm.Meta):
        model = models.AnuncioIndustrial
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'metros_cuadrados',
            'type_anuncio',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )


class AnuncioLocalForm(BaseAnuncioForm):

    class Meta(BaseAnuncioForm.Meta):
        model = models.AnuncioLocal
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'metros_cuadrados',
            'type_anuncio',
            'description',
            'precio',
            'is_premium',
            'latitude',
            'longitude',
        )
