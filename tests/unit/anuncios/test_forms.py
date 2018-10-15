import os

from django import forms

from anuncios import forms as anuncios_form
from anuncios.models import Anuncio
from tests.unit.base_test import BaseTestCase


class AnuncioFormTestMixin(object):

    def setUp(self):
        super().setUp()
        path_data = os.path.join(os.path.dirname(__file__), 'anuncio.json')
        self.form_data = self.load_data(path_data)

    def get_form(self, category):
        """Wrapper para obtener una clase de anuncios_form.

        Args:
            category (str): Valor de las contantes Anuncio.CATEGORY_CHOICES.

        Returns:
            BaseAnuncioForm: Subclase
        """
        category = category.upper()
        if not hasattr(Anuncio, category):
            raise NotImplementedError
        return anuncios_form.BaseAnuncioForm.get_form_class(getattr(Anuncio, category))


class BaseAnuncioFormTest(AnuncioFormTestMixin, BaseTestCase):
    """El archivo anuncio.json contiene datos para cualquier
    tipo de form.
    """

    def test_fields_not_required(self):
        """Comprueba los fields required = False."""
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
        fields_not_required_in_form = anuncios_form.BaseAnuncioForm.fields_not_required

        # La prueba se hace en los dos sentidos.
        for field in fields_not_required:
            self.assertIn(field, fields_not_required_in_form)
        for field in fields_not_required_in_form:
            self.assertIn(field, fields_not_required)

    def test_fields_hidden(self):
        """Prueba de los campos que son ocultos."""
        fields_hidden = ['owner', 'category', 'is_premium', 'latitude', 'longitude']
        fields_hidden_in_form = anuncios_form.BaseAnuncioForm.fields_hidden

        # La prueba se hace en los dos sentidos.
        for field in fields_hidden:
            self.assertIn(field, fields_hidden_in_form)
        for field in fields_hidden_in_form:
            self.assertIn(field, fields_hidden)

    def test_loacalized_fields(self):
        """Prueba del campo Meta localized_fields."""
        localized_fields = anuncios_form.BaseAnuncioForm.Meta.localized_fields
        self.assertIn('precio', localized_fields)
        self.assertIn('metros_cuadrados', localized_fields)
        self.assertIn('ano_construccion', localized_fields)

    def test_help_text(self):
        """Prueba de los help_texts."""
        help_texts = {
            'address': 'Si quieres mantener la privacidad, pon solo la calle.',
            'phone': 'Si no se añade, solo se podrá contactar por mensaje privado.',
            'description': 'Cualquier descripción que quieras aportar.',
            'genero': '¿Buscas un genero concreto?',
            'permite_fumar_piso': '¿Se permite fumar en la vivienda?',
            'permite_fumar_habitacion': '¿Se permite fumar en la habitación?'
        }
        help_texts_in_form = anuncios_form.BaseAnuncioForm.Meta.help_texts

        # La prueba se hace en los dos sentidos.
        for field, text in help_texts.items():
            self.assertEqual(help_texts[field], help_texts_in_form[field])
            self.assertEqual(text, help_texts_in_form[field])
        for field, text in help_texts_in_form.items():
            self.assertEqual(help_texts[field], help_texts[field])
            self.assertEqual(text, help_texts[field])

    def test_clean_precio(self):
        """Los precios han de ser > 0."""
        form_class = self.get_form('piso')
        form = form_class(data=self.form_data)

        self.assertTrue(form.is_valid())

        # Poner el precio a 0 y debería fallar.
        self.form_data['precio'] = 0
        form = form_class(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_clean_metros_cuadrados(self):
        """Metros cuadrados ha de ser > 0."""
        form_class = self.get_form('piso')
        form = form_class(data=self.form_data)

        self.assertTrue(form.is_valid())

        # Poner el precio a 0 y debería fallar.
        self.form_data['metros_cuadrados'] = 0
        form = form_class(data=self.form_data)
        self.assertFalse(form.is_valid())


class BaseAnuncioViviendaFormTest(AnuncioFormTestMixin, BaseTestCase):
    """Prueba los clean y los campos que debe tener."""

    def test_fields(self):
        """Prueba los fields que necesita el form."""
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
            'precio',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.BaseAnuncioViviendaForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_clean_estado_inmueble(self):
        """Test para el estado de inmueble.

        Dependiendo de si es una compra o no, el campo
        es requerido o no.
        VENTA = SI
        ALQUILER = NO
        """
        form_class = self.get_form('piso')
        self.form_data['type_anuncio'] = Anuncio.VENTA
        self.form_data['estado_inmueble'] = Anuncio.OBRANUEVA
        form = form_class(data=self.form_data)

        # Requiere del campo estado_inmueble.
        self.assertTrue(form.is_valid())

        self.form_data['estado_inmueble'] = None
        form = form_class(data=self.form_data)

        # Tiene que fallar por que no tiene estado_inmueble.
        self.assertFalse(form.is_valid())

    def test_clean_habitaciones(self):
        """Las viviendas requieren de habitaciones > 0."""
        form_class = self.get_form('piso')
        self.form_data['habitaciones'] = 0
        form = form_class(data=self.form_data)

        # Requiere que habitaciones sea > 0
        self.assertFalse(form.is_valid())

    def test_clean_banos(self):
        """Las viviendas requieren de habitaciones > 0."""
        form_class = self.get_form('piso')
        self.form_data['banos'] = 0
        form = form_class(data=self.form_data)

        # Requiere que banos sea > 0
        self.assertFalse(form.is_valid())


class AnuncioPisoFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('piso'))


class AnuncioCasaFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('casa'))


class AnuncioApartamentoFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('apartamento'))


class AnuncioHabitacionFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_fields(self):
        """Prueba los fields que deben contener el form."""
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'owner',
            'category',
            'phone',
            'precio',
            'type_anuncio',
            'genero',
            'internet',
            'permite_fumar_piso',
            'permite_fumar_habitacion',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.AnuncioHabitacionForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('habitacion'))

    def test_type_anuncio(self):
        """El field type_anuncio ha de ser hidden y el
        valor por defecto a de ser Anuncio.ALQUILER.
        """
        form_class = self.get_form('habitacion')
        form = form_class()

        self.assertEqual(
            type(form.fields['type_anuncio'].widget),
            type(forms.HiddenInput())
        )
        self.assertEqual(form.initial['type_anuncio'], Anuncio.ALQUILER)


class AnuncioTerrenoFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_fields(self):
        """Prueba los fields que deben contener el form."""
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
            'precio',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.AnuncioTerrenoForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('terreno'))


class AnuncioParkingFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_fields(self):
        """Prueba los fields que deben contener el form."""
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
            'precio',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.AnuncioParkingForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('parking'))


class AnuncioIndustrialFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_fields(self):
        """Prueba los fields que deben contener el form."""
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
            'precio',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.AnuncioIndustrialForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('industrial'))


class AnuncioLocalFormTest(AnuncioFormTestMixin, BaseTestCase):

    def test_fields(self):
        """Prueba los fields que deben contener el form."""
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
            'precio',
            'description',
            'is_premium',
            'latitude',
            'longitude',
        )
        fields_in_form = anuncios_form.AnuncioLocalForm.Meta.fields

        # La prueba se hace en los dos sentidos.
        for field in fields:
            self.assertIn(field, fields_in_form)
        for field in fields_in_form:
            self.assertIn(field, fields)

    def test_get_form_class(self):
        """Se obtiene el form class."""
        self.assertTrue(self.get_form('local'))
