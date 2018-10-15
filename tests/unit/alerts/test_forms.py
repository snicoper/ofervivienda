from django.forms.fields import TypedChoiceField
from django.forms.widgets import HiddenInput

from alerts import forms
from alerts.models import AlertAnuncio

from .base_alerts import BaseTestAlerts


class BaseAlertFormTest(BaseTestAlerts):

    def test_get_form_class(self):
        """Comprueba que existe un form para cada categoría.

        La convención de nombres es Alert{Category}Form.
        """
        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.PISO)
        self.assertEqual(type(form_class), type(forms.AlertPisoForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.CASA)
        self.assertEqual(type(form_class), type(forms.AlertCasaForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.APARTAMENTO)
        self.assertEqual(type(form_class), type(forms.AlertApartamentoForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.HABITACION)
        self.assertEqual(type(form_class), type(forms.AlertHabitacionForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.TERRENO)
        self.assertEqual(type(form_class), type(forms.AlertTerrenoForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.PARKING)
        self.assertEqual(type(form_class), type(forms.AlertTerrenoForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.INDUSTRIAL)
        self.assertEqual(type(form_class), type(forms.AlertIndustrialForm))

        form_class = forms.BaseAlertForm.get_form_class(AlertAnuncio.LOCAL)
        self.assertEqual(type(form_class), type(forms.AlertLocalForm))


class BaseViviendaFormTest(BaseTestAlerts):
    """Prueba pisos, casas y apartamentos."""

    def setUp(self):
        super().setUp()
        self.required_fields = [
            'category',
            'owner',
            'polygon',
            'latitude',
            'longitude',
            'description'
        ]

    def test_campos_requeridos(self):
        """Comprueba los campos requeridos."""
        copy_form = self.form_data
        form = forms.AlertPisoForm(data=copy_form)

        self.assertTrue(form.is_valid())

        # Si falta un campo, form no valido.
        for field in self.required_fields:
            copy_form[field] = None
            form = forms.AlertPisoForm(data=copy_form)
            self.assertFalse(form.is_valid())
            copy_form[field] = self.form_data[field]

    def test_required_fields(self):
        """Prueba el form solo con los campos required_fields."""
        form_data = {}
        for field in self.required_fields:
            form_data[field] = self.form_data[field]
        form = forms.AlertPisoForm(data=form_data)
        self.assertTrue(form.is_valid())


class AlertHabitacionFormTest(BaseTestAlerts):

    def test_prueba_exista_fields(self):
        """Comprueba los campos para habitaciones."""
        alert = forms.AlertHabitacionForm()
        fields = alert.fields

        self.assertIn('genero', fields)
        self.assertIn('permite_fumar_piso', fields)
        self.assertIn('permite_fumar_habitacion', fields)
        self.assertIn('internet', fields)

    def test_type_anuncio_hidden_y_initial(self):
        """Prueba que type_anuncio sea un campo hidden y su valor."""
        alert = forms.AlertHabitacionForm()
        fields = alert.fields

        self.assertIsInstance(fields['type_anuncio'], TypedChoiceField)
        self.assertEqual(type(fields['type_anuncio'].widget), HiddenInput)
        self.assertEqual(alert.initial['type_anuncio'], AlertAnuncio.ALQUILER)
