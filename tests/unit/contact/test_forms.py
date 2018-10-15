from contact.forms import ContactForm

from .base_contact import BaseContactTest


class ContactFormTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        self.form_data = {
            'subject': 'Mensaje test',
            'message': 'Mensaje de prueba',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        self.form = ContactForm(data=self.form_data)

    def test_form_valid(self):
        """Todos los campos son requeridos."""
        self.assertTrue(self.form.is_valid())

        # Sin campo subject.
        form_data = self.form_data
        form_data['subject'] = ''
        form = ContactForm(data=form_data)

        self.assertFalse(form.is_valid())

        # Sin campo message.
        form_data = self.form_data
        form_data['message'] = ''
        form = ContactForm(data=form_data)

        self.assertFalse(form.is_valid())

        # Sin campo username.
        form_data = self.form_data
        form_data['username'] = ''
        form = ContactForm(data=form_data)

        self.assertFalse(form.is_valid())

        # Sin campo username.
        form_data = self.form_data
        form_data['email'] = ''
        form = ContactForm(data=form_data)

        self.assertFalse(form.is_valid())
