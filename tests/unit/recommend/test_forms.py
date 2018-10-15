from django.test import TestCase

from recommend.forms import RecommendForm


class RecommendFormTest(TestCase):

    def setUp(self):
        super().setUp()
        self.form_data = {
            'email_to': 'email1@example.com',
            'from_email': 'email2@example.com',
            'body': 'Test message'
        }
        self.form = RecommendForm(data=self.form_data)

    def test_form_valid(self):
        """Form valido."""
        self.assertTrue(self.form.is_valid())

    def test_todos_los_campos_son_requeridos(self):
        """Todos los campos en el form son requeridos."""
        # email_to
        copy_form_data = self.form_data
        copy_form_data['email_to'] = ''
        form = RecommendForm(data=copy_form_data)

        self.assertFalse(form.is_valid())

        # from_email
        copy_form_data = self.form_data
        copy_form_data['from_email'] = ''
        form = RecommendForm(data=copy_form_data)

        self.assertFalse(form.is_valid())

        # body
        copy_form_data = self.form_data
        copy_form_data['body'] = ''
        form = RecommendForm(data=copy_form_data)

        self.assertFalse(form.is_valid())
