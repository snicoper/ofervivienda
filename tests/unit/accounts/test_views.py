import os

from django.urls import reverse

from PIL import Image

from accounts.models import UserLocation, UserOptions
from config.settings import test as settings_test
from tests.unit.images import simple_uploaded_file

from .base_accounts import BaseAccountsTest


class UserProfileViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:profile'
        self.url = reverse(self.urlconf)
        self.login()

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        redirect_to = '{}?next={}'.format(
            self.test_settings.LOGIN_URL,
            self.url
        )
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=redirect_to,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/profile.html')


class UserProfilePublicViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:profile_public'
        self.url = reverse(self.urlconf, kwargs={'slug': 'perico'})

    def test_usuario_anonimo(self):
        """Todo el mundo puede ver el perfil."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/profile_public.html')

    def test_get_context_data(self):
        """Requiere del form para crear pmessages."""
        response = self.client.get(self.url)
        context = response.context
        profile = context['profile']
        user = context['user']

        self.assertIn('form', context)

        # Comprobar los datos iniciales.
        initial = context['form'].initial
        self.assertEqual(initial['sender'], user)
        self.assertEqual(initial['recipient'], profile)


class UserProfileUpdateViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:profile_update'
        self.url = reverse(self.urlconf)
        self.login()

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona Http404."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/profile_update.html')

    def test_update_phone(self):
        """Actualiza el teléfono."""
        telefono = self.user.phone
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['phone'] = '666 666 666'
        response = self.client.post(self.url, data=form, follow=True)
        new_telefono = self.user_model.objects.get(pk=1)

        # El teléfono ha tenido que cambiar.
        self.assertNotEqual(telefono, new_telefono)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:profile'),
            status_code=302,
            target_status_code=200
        )


class UserAvatarUpdateViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:avatar_update'
        self.url = reverse(self.urlconf)
        self.login()
        avartarpath = os.path.join(os.path.dirname(__file__), 'avatar.jpg')
        with open(avartarpath, 'rb') as fh:
            self.image = fh.read()
        self.avatar = simple_uploaded_file(avartarpath)
        self.save_path = os.path.join(
            settings_test.MEDIA_ROOT,
            self.accounts_settings.ACCOUNTS_AVATAR_PATH,
            'avatar.jpg'
        )
        self.form_data = {
            'avatar': self.avatar
        }

    def tearDown(self):
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_status_code_302_post(self):
        """Comprueba el estatus code cuando se actualiza."""
        response = self.client.post(self.url, data=self.form_data, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:profile'),
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/avatar_update.html')

    def test_campo_delete_avatar_en_get(self):
        """Si no tiene avatar, el campo delete_avatar estará oculto."""
        delete_avatar = self.client.get(self.url).context['form'].fields['delete_avatar']

        self.assertEqual(delete_avatar.widget.__class__.__name__, 'HiddenInput')

    def test_form_post(self):
        """Prueba cuando se maneja el avatar en method post."""
        expected_width = self.accounts_settings.ACCOUNTS_AVATAR_WIDTH
        expected_height = self.accounts_settings.ACCOUNTS_AVATAR_HEIGHT
        self.client.post(self.url, data=self.form_data, follow=True)

        with Image.open(self.save_path) as fh:
            image = fh

        width, height = image.size

        # Comprueba el tamaño haya cambiado.
        self.assertLessEqual(width, expected_width)
        self.assertLessEqual(height, expected_height)

        # Cuando se ha subido una imagen, al volver al form el campo delete_avatar,
        # no debe ser HiddenInput.
        delete_avatar = self.client.get(self.url).context['form'].fields['delete_avatar']

        self.assertEqual(delete_avatar.widget.__class__.__name__, 'CheckboxInput')

    def test_delete_avatar_elimina_imagen_en_disco(self):
        """Cuando selecciona delete_avatar, la imagen sera eliminada."""
        self.client.post(self.url, data=self.form_data)
        initial = self.client.get(self.url).context['form'].initial

        self.assertTrue(os.path.exists(self.save_path))

        # Comprueba que elimina la imagen del disco si pulsa en la opción
        # delete_avatar.
        initial['delete_avatar'] = 'true'
        self.client.post(self.url, data=initial)

        self.assertFalse(os.path.exists(self.save_path))


class UserOptionsDetailViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:options'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        self.assertEqual(self.response.status_code, 200)

    def test_templete_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'accounts/profile_options.html')

    def test_context_object(self):
        """Prueba el nombre del context_object_name y el tipo."""
        context = self.response.context['options']
        user = self.response.context['user']

        self.assertTrue(context)
        self.assertIsInstance(context, UserOptions)
        self.assertEqual(context.user, user)


class UserOptionsUpdateViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:options_update'
        self.url = reverse(self.urlconf)
        self.login()

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_status_code_302_post(self):
        """Comprueba el estatus code cuando se actualiza."""
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['phone_public'] = not form['phone_public']
        response = self.client.post(self.url, data=form, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:options'),
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/options_update.html')

    def test_estados_por_defectos(self):
        """Comprueba los estados por defectos."""
        user_options = self.user.user_options

        # Email public.
        self.assertFalse(user_options.email_public)

        # Dirección publica.
        self.assertFalse(user_options.address_public)

        # Teléfono publica.
        self.assertFalse(user_options.phone_public)

    def test_cambia_los_estados(self):
        """Cambia los estados al contrario al actual."""
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['phone_public'] = not form['phone_public']
        form['address_public'] = not form['address_public']
        form['email_public'] = not form['email_public']
        self.client.post(self.url, data=form)
        user_options = self.user_model.objects.get(pk=1).user_options

        # Email public.
        self.assertTrue(user_options.email_public)

        # Dirección publica.
        self.assertTrue(user_options.address_public)

        # Teléfono publica.
        self.assertTrue(user_options.phone_public)


class UserLocationDetailViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:location'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""

        self.assertEqual(self.response.status_code, 200)

    def test_templete_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'accounts/profile_location.html')

    def test_context_object(self):
        """Prueba el nombre del context_object_name y el tipo."""
        context = self.response.context['location']
        user = self.response.context['user']

        self.assertTrue(context)
        self.assertIsInstance(context, UserLocation)
        self.assertEqual(context.user, user)


class UserLocationUpdateViewTest(BaseAccountsTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'accounts:location_update'
        self.url = reverse(self.urlconf)
        self.login()
        datapath = os.path.join(os.path.dirname(__file__), 'localization.json')
        self.data = self.load_data(datapath)

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_por_defecto_los_campos_estan_vacios(self):
        """Por defecto todos los campos están vacíos."""
        user_location = self.user_model.objects.get(pk=1).user_location

        self.assertFalse(user_location.country)
        self.assertFalse(user_location.state)
        self.assertFalse(user_location.city)
        self.assertFalse(user_location.address)
        self.assertFalse(user_location.zipcode)
        self.assertFalse(user_location.latitude)
        self.assertFalse(user_location.longitude)
        self.assertFalse(user_location.point)

    def test_method_post(self):
        """Comprueba la actualización de datos."""
        response = self.client.post(self.url, data=self.data, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:location'),
            status_code=302,
            target_status_code=200
        )

        # Comprueba que se han guardado los campos.
        user_location = self.user_model.objects.get(pk=1).user_location

        self.assertTrue(user_location.country)
        self.assertTrue(user_location.state)
        self.assertTrue(user_location.city)
        self.assertTrue(user_location.address)
        self.assertTrue(user_location.zipcode)
        self.assertTrue(user_location.latitude)
        self.assertTrue(user_location.longitude)
        self.assertTrue(user_location.point)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/location_update.html')
