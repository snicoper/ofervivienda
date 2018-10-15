import os

from django.forms import widgets
from django.utils.crypto import get_random_string

from accounts import forms
from authentication.models import RegisterUser
from tests.unit.base_test import BaseTestCase


class UserProfileUpdateFormTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.form = forms.UserProfileUpdateForm
        self.form_data = {
            'phone': '111 222 333',
            'public_name': 'Test User',
            'description': 'Hola mundo!'
        }

    def test_form_valid(self):
        """Prueba un form valido."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_ningun_campo_es_requerido(self):
        """Ningún campo es obligatorio."""
        form = self.form(data={})

        self.assertTrue(form.is_valid())


class UserCreationFormTest(BaseTestCase):
    """Form en la administración de Django."""

    def setUp(self):
        super().setUp()
        self.form = forms.UserCreationForm
        self.form_data = {
            'username': 'test',
            'password1': 'TestUser1234',
            'password2': 'TestUser1234',
            'email': 'test@example.com'
        }

    def test_form_valid(self):
        """Un form valido."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_username(self):
        """Comprueba el campo username."""
        self.form_data['username'] = self.user.username
        form = self.form(data=self.form_data)

        # Username ya existe.
        self.assertFalse(form.is_valid())

        # Message error para username ya existe.
        errors = form.errors
        self.assertEqual(
            errors['username'][0],
            'El usuario ya existe en usuarios o registro temporal.'
        )

        # Comprueba si el Email ya existe en la tabla temporal form no valid.
        RegisterUser.objects.create(
            username='testnewuser@example.com',
            email='test12@example.com',
            password='12333221',
            token=get_random_string(length=32)
        )
        self.form_data['username'] = 'testnewuser@example.com'
        form = self.form(data=self.form_data)

        # Username ya existe.
        self.assertFalse(form.is_valid())

        # Message error para username ya existe.
        errors = form.errors
        self.assertEqual(
            errors['username'][0],
            'El usuario ya existe en usuarios o registro temporal.'
        )

    def test_email(self):
        """Comprueba el campo username."""
        self.form_data['email'] = self.user.email
        form = self.form(data=self.form_data)

        # Username ya existe.
        self.assertFalse(form.is_valid())

        # Message error para Email ya existe.
        errors = form.errors
        self.assertEqual(
            errors['email'][0],
            'El Email ya existe en usuarios o registro temporal.'
        )

        # Comprueba si el Email ya existe en la tabla temporal form no valid.
        RegisterUser.objects.create(
            username='testnewuser@example.com',
            email='test12@example.com',
            password='12333221',
            token=get_random_string(length=32)
        )
        self.form_data['email'] = 'test12@example.com'
        form = self.form(data=self.form_data)

        # Username ya existe.
        self.assertFalse(form.is_valid())

        # Message error para username ya existe.
        errors = form.errors
        self.assertEqual(
            errors['email'][0],
            'El Email ya existe en usuarios o registro temporal.'
        )


class UserOptionsFormTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.form = forms.UserOptionsForm
        self.form_data = {
            'phone_public': 'true',
            'address_public': 'true',
            'email_public': 'true',
            'notify_precio_anuncio_baja': 'true'
        }

    def test_form_valid(self):
        """Comprueba el form, ningún campo es obligatorio."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

        form = self.form(data={})

        self.assertTrue(form.is_valid())


class UserUpdateAvatarFormTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.form = forms.UserUpdateAvatarForm
        self.form_data = {
            'delete_avatar': 'false',
            'avatar': 'avatar.png'
        }

    def test_form_valid(self):
        """Comprueba el form, ningún campo es obligatorio."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

        form = self.form(data={})

        self.assertTrue(form.is_valid())


class UserLocationUpdateFormTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.form = forms.UserLocationUpdateForm

        # load data
        localization_path = os.path.join(os.path.dirname(__file__), 'localization.json')
        self.form_data = self.load_data(localization_path)

    def test_form_valid(self):
        """Form valido."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_todos_los_campos_son_requeridos(self):
        """Todos los campos son requeridos."""
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'latitude',
            'longitude'
        )

        copy_form_data = self.form_data.copy()

        for field in fields:
            copy_form_data[field] = ''
            form = self.form(data=copy_form_data)
            self.assertFalse(form.is_valid())
            self.copy_form_data = self.form_data[field]

    def test_lat_and_lng_hidden_fields(self):
        """Los campos latitude y longitude son HiddenInput."""
        form = self.form(data=self.form_data)
        latitude = form.fields['latitude'].widget
        longitude = form.fields['longitude'].widget

        self.assertIsInstance(latitude, widgets.HiddenInput)
        self.assertIsInstance(longitude, widgets.HiddenInput)
