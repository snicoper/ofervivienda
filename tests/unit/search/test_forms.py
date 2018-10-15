from django import forms as django_forms

from anuncios import models
from search import forms

from .base_search import BaseSearchTest


class SearchAddressFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form_data = {
            'q': 'granollers',
            'category': self.anuncio_model.PISO,
            'type_anuncio': self.anuncio_model.VENTA
        }

    def test_form_valid(self):
        """El form con todos los campos es valido."""
        form = forms.SearchAddressForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_requiere_todos_los_campos(self):
        """El form para ser valido, require de datos en todos los campos."""
        # Campo q
        form_data = self.form_data.copy()
        form_data['q'] = ''
        form = forms.SearchAddressForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Campo category
        form_data = self.form_data.copy()
        form_data['category'] = ''
        form = forms.SearchAddressForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Campo type_anuncio
        form_data = self.form_data.copy()
        form_data['type_anuncio'] = ''
        form = forms.SearchAddressForm(data=form_data)
        self.assertFalse(form.is_valid())


class BaseSearchFormTest(BaseSearchTest):
    """Al ser un form Base, no tiene un model, ya que este form no es para
    instanciar.
    Si se intenta instanciar directamente dará un error.
    """

    def test_localized_fields(self):
        """Campos localized_fields."""
        localized_fields = ('precio', 'metros_cuadrados')
        localized_fields_form = forms.BaseSearchForm.Meta.localized_fields

        for field in localized_fields_form:
            if field not in localized_fields:
                msg_error = '{} no implementado en BaseSearchForm.Meta.localized_fields'.format(
                    field
                )
                raise NotImplementedError(msg_error)

    def test_help_text(self):
        """Prueba los help_texts."""
        help_texts = forms.BaseSearchForm.Meta.help_texts

        self.assertEqual(help_texts['metros_cuadrados'], 'Metros cuadrados mínimo')
        self.assertEqual(help_texts['habitaciones'], 'Habitaciones mínimo')
        self.assertEqual(help_texts['banos'], 'Baños mínimo')
        self.assertEqual(help_texts['precio'], 'Precio máximo')

    def test_no_instanciable(self):
        """El form no se puede instanciar directamente."""
        with self.assertRaises(ValueError):
            forms.BaseSearchForm()

    def test_get_instance_subclass(self):
        """Obtener una instancia de una de las subclases según category."""
        # Piso
        form = forms.BaseSearchForm.get_form_class('piso')()
        self.assertIsInstance(form, forms.SearchPisoForm)

        # Casa
        form = forms.BaseSearchForm.get_form_class('casa')()
        self.assertIsInstance(form, forms.SearchCasaForm)

        # Apartamento, da igual upper, lower, etc
        form = forms.BaseSearchForm.get_form_class('aParTaMento')()
        self.assertIsInstance(form, forms.SearchApartamentoForm)

        # Habitacion
        form = forms.BaseSearchForm.get_form_class('Habitacion')()
        self.assertIsInstance(form, forms.SearchHabitacionForm)

        # Terreno
        form = forms.BaseSearchForm.get_form_class('terreno')()
        self.assertIsInstance(form, forms.SearchTerrenoForm)

        # Parking
        form = forms.BaseSearchForm.get_form_class('parKing')()
        self.assertIsInstance(form, forms.SearchParkingForm)

        # Nave Industrial
        form = forms.BaseSearchForm.get_form_class('industrial')()
        self.assertIsInstance(form, forms.SearchIndustrialForm)

        # Locales
        form = forms.BaseSearchForm.get_form_class('local')()
        self.assertIsInstance(form, forms.SearchLocalForm)

    def test_si_no_existe_subclase_return_none(self):
        """Si una subclase no existe, retorna None."""
        form = forms.BaseSearchForm.get_form_class('noexisto')
        self.assertIsNone(form)


class BaseViviendaFormTest(BaseSearchTest):
    """Este form no es instanciable, por lo que solo prueba los campos
    Meta.fields.
    """

    def test_meta_fields(self):
        """Prueba los fields de Meta."""
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
        fields_form = forms.BaseViviendaForm.Meta.fields

        # Prueba que tengan el mismo numero de campos."""
        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en BaseViviendaForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)


class SearchPisoFormTest(BaseSearchTest):
    """Este test comprueba los hidden_fields de BaseSearchForm.

    BaseSearchForm como no es instanciable, no se pudo probar.
    """

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('piso')()

    def test_hidden_fields_de_BaseSearchForm(self):
        """Prueba los campos hidden_fields de BaseSearchForm."""
        hidden_fields = ['latitude', 'longitude']

        # Numero de campos iguales.
        self.assertEqual(len(hidden_fields), len(self.form.hidden_fields()))

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioPiso)


class SearchCasaFormTest(BaseSearchTest):

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        form = forms.BaseSearchForm.get_form_class('casa')()
        self.assertEqual(form.Meta.model, models.AnuncioCasa)


class SearchApartamentoFormTest(BaseSearchTest):

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        form = forms.BaseSearchForm.get_form_class('Apartamento')()
        self.assertEqual(form.Meta.model, models.AnuncioApartamento)


class SearchHabitacionFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('Habitacion')()

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioHabitacion)

    def test_fields(self):
        """Comprueba los fields de habitaciones."""
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
        fields_form = self.form.fields

        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en SearchAddressForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)

    def test_field_type_anuncio_HiddenInput(self):
        """El campo type_anuncio es HiddenInput."""
        self.assertIsInstance(self.form.fields['type_anuncio'].widget, django_forms.HiddenInput)

    def test_fields_type_anuncio_initial(self):
        """El campo type_anuncio, el initial es Anuncio.ALQUILER."""
        self.assertEqual(self.form.initial['type_anuncio'], self.anuncio_model.ALQUILER)


class SearchTerrenoFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('terreno')()

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioTerreno)

    def test_meta_fields(self):
        """Prueba los campos de Meta.fields."""
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )
        fields_form = self.form.fields

        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en SearchTerrenoForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)


class SearchParkingFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('parKing')()

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioParking)

    def test_meta_fields(self):
        """Prueba los campos de Meta.fields."""
        fields = (
            'category',
            'q',
            'type_anuncio',
            'precio',
            'latitude',
            'longitude',
        )
        fields_form = self.form.fields

        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en SearchParkingForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)


class SearchIndustrialFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('industrial')()

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioIndustrial)

    def test_meta_fields(self):
        """Prueba los campos de Meta.fields."""
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )
        fields_form = self.form.fields

        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en SearchIndustrialForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)


class SearchLocalFormTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.form = forms.BaseSearchForm.get_form_class('local')()

    def test_model_form(self):
        """Prueba Form.Meta.model."""
        self.assertEqual(self.form.Meta.model, models.AnuncioLocal)

    def test_meta_fields(self):
        """Prueba los campos de Meta.fields."""
        fields = (
            'category',
            'q',
            'type_anuncio',
            'metros_cuadrados',
            'precio',
            'latitude',
            'longitude',
        )
        fields_form = self.form.fields

        self.assertEqual(len(fields), len(fields_form))

        for field in fields:
            msg_error = '{} no implementado en SearchLocalForm.Meta.fields'.format(field)
            if field not in fields_form:
                raise NotImplementedError(msg_error)
