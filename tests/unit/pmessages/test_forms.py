import os

from django.forms.widgets import HiddenInput

from pmessages.forms import MessageCreateForm

from .base_pmessages import BasePmessagesTest


class MessageCreateFormTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.form = MessageCreateForm
        self.form_data = self.load_data(
            os.path.join(os.path.dirname(__file__), 'pmessages_data.json')
        )

    def test_form_valid(self):
        """Prueba un form valido."""
        form = self.form(self.form_data)

        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """Prueba casos donde el form no es valido."""
        # El campo subject es requerido.
        self.form_data['subject'] = ''
        form = self.form(self.form_data)

        self.assertFalse(form.is_valid())

        # subject requiere de al menos 10 caracteres
        self.form_data['subject'] = 'abc'
        form = self.form(self.form_data)

        self.assertFalse(form.is_valid())

        # El campo body es requerido.
        self.form_data['body'] = ''
        form = self.form(self.form_data)

        self.assertFalse(form.is_valid())

        # body requiere de al menos 10 caracteres
        self.form_data['body'] = 'abc'
        form = self.form(self.form_data)

        self.assertFalse(form.is_valid())

    def test_campos_hidden(self):
        """Campos que requieren que sean HiddenInput."""
        fields = self.form(self.form_data).fields

        self.assertEqual(type(fields['parent'].widget), HiddenInput)
        self.assertEqual(type(fields['anuncio'].widget), HiddenInput)
        self.assertEqual(type(fields['sender'].widget), HiddenInput)
        self.assertEqual(type(fields['recipient'].widget), HiddenInput)
