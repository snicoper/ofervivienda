import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from dateutil import relativedelta

from accounts import settings as accounts_settings
from tests.unit.images import simple_uploaded_file

# Vars
UserModel = get_user_model()
image_path = os.path.join(os.path.dirname(__file__), 'avatar.jpg')


class UserTest(TestCase):
    """Test para model User."""

    def setUp(self):
        super().setUp()
        self.username = 'testuser'
        self.password = '123'
        self.email = 'usertest@example.com'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )
        self.image_avatar = simple_uploaded_file(image_path)

    def test_usuario_simple_creado(self):
        """Crea un un usuario y lo comprueba."""
        # Usuario se ha creado.
        self.assertTrue(self.user)

        # Username.
        self.assertEqual(self.user.username, self.username)

        # Email.
        self.assertEqual(self.user.email, self.email)

        # Password no es igual (se ha hasheado).
        self.assertNotEqual(self.user.password, self.password)

        # No tiene avatar.
        self.assertFalse(self.user.avatar)

        # Sin public_name
        self.assertFalse(self.user.public_name)

        # Campo phone es empty.
        self.assertEqual(self.user.phone, '')

        # Campo description es empty.
        self.assertEqual(self.user.description, '')

        # El usuario no es Premium.
        self.assertFalse(self.user.is_premium)

        # anuncios_premium tiene el valor 0.
        self.assertEqual(self.user.anuncios_premium, 0)

        # Fecha expire_premium_at es menor a now()
        self.assertTrue(self.user.expire_premium_at < timezone.now())

    def test_str(self):
        """Método __str__ obtiene el username."""
        self.assertEqual(str(self.user), self.username)

    def test_get_public_username(self):
        """Si tiene el public_name lo devuelve, si no, el username."""
        self.assertEqual(self.user.get_public_name, self.username)
        self.user.public_name = 'Test User'
        self.user.save()
        user = UserModel.objects.get(pk=self.user.pk)

        self.assertEqual(user.get_public_name, 'Test User')

    def test_slug_username(self):
        """Se ha generado el slug."""
        self.assertTrue(self.user.slug)

    def test_anadir_o_actualizar_avatar(self):
        """Comprobación de añadir/cambios de avatar.

        Puede dar un falso error, si es así, limpiar el directorio
        src/media/test/accounts/avatar
        """
        user = UserModel(
            username='testavatar',
            email='testavatar@example.com',
            password='123456',
            avatar=self.image_avatar
        )
        user.save()

        user_avatar = user.avatar

        # El usuario ahora tiene un avatar.
        self.assertTrue(user_avatar)

        # Dimensiones de la imagen.
        self.assertLessEqual(user_avatar.width, accounts_settings.ACCOUNTS_AVATAR_WIDTH)
        self.assertLessEqual(user_avatar.height, accounts_settings.ACCOUNTS_AVATAR_HEIGHT)

        # Al actualizar una imagen, se elimina la anterior.
        old_avatar_name = user.avatar.name
        old_avatar_path = user.avatar.path
        user.avatar = self.image_avatar
        user.save()
        new_avatar_name = user.avatar.name
        new_avatar_path = user.avatar.path

        self.assertNotEqual(old_avatar_name, new_avatar_name)
        self.assertNotEqual(old_avatar_path, new_avatar_path)

        # old_avatar_path se ha eliminado del disco.
        self.assertFalse(os.path.exists(old_avatar_path))

        # Eliminar un avatar, elimina la imagen en disco también.
        user.avatar = None
        user.save()

        self.assertFalse(os.path.exists(new_avatar_path))

    def test_eliminar_usuario_elimina_avatar(self):
        """Si se elimina un usuario, el avatar se elimina del disco."""
        user = UserModel(
            username='testavatar',
            email='testavatar@example.com',
            password='123456',
            avatar=self.image_avatar
        )
        user.save()
        image_path = user.avatar.path

        # Existe valor para self.avatar.path.
        self.assertTrue(user.avatar.path)

        # La imagen estan en el path.
        self.assertTrue(os.path.exists(image_path))

        # Eliminar usuario.
        user.delete()

        self.assertFalse(os.path.exists(image_path))

    def test_update_premium(self):
        """update_premium se incrementa en X meses."""
        old_expire_premium = self.user.expire_premium_at
        self.user.update_premium(1)

        # El método, no debe guardar los cambios.
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.expire_premium_at, old_expire_premium)

        self.user.save()

        # Se ha incrementado la fecha de expiración.
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertTrue(old_expire_premium < user.expire_premium_at)

        # El resultado es 1 meses mas que old_expire_premium.
        # Cuando un usuario tiene expirado el tiempo, al llamar a update_premium
        # el tiempo se actualiza a now.
        time_future = timezone.now() + relativedelta.relativedelta(months=1)
        date_format = '%d %m %Y %H'
        date_now = self.user.expire_premium_at.strftime(date_format)
        date_future = time_future.strftime(date_format)

        self.assertEqual(date_now, date_future)

    def test_incrementar_num_anuncios_premium(self):
        """Incrementar en 1 el numero de anuncios Premium."""
        self.user.increase_anuncio()

        # El método no debe guardar la actualización.
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.anuncios_premium, 0)

        # Se incrementa en 1.
        self.user.save()
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.anuncios_premium, 1)

    def test_decrementar_num_anuncios_premium(self):
        """Incrementar en 1 el numero de anuncios Premium."""
        # Si el valor actual es 0, no hace nada
        user = UserModel.objects.filter(username=self.username)[0]
        user.decrease_anuncio()

        self.assertEqual(user.anuncios_premium, 0)
        del user

        # Incrementar en 2 los anuncios Premium.
        self.user.increase_anuncio()
        self.user.increase_anuncio()
        self.user.save()
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.anuncios_premium, 2)
        del user

        # El método no debe guardar la actualización.
        self.user.decrease_anuncio()
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.anuncios_premium, 2)
        del user

        # Se decrementa en 1.
        self.user.save()
        user = UserModel.objects.filter(username=self.username)[0]
        self.assertEqual(user.anuncios_premium, 1)


class AccountsSignalsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.username = 'testuser'
        self.password = '123'
        self.email = 'usertest@example.com'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_user_options_es_creado_al_crear_usuario(self):
        """Comprueba que UserOptions se ha creado."""
        self.assertTrue(self.user.user_options)

    def test_favorites_es_creado_al_crear_usuario(self):
        """Comprueba que Favorites es creado."""
        self.assertTrue(self.user.favorites_user)

    def test_user_locations_es_creado_al_crear_usuario(self):
        """Comprueba que UserLocation se ha creado."""
        self.assertTrue(self.user.user_location)


class UserLocationTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user = UserModel.objects.create_user(
            username='test_user',
            password='123',
            email='test_user@example.com'
        )

    def test_str(self):
        """Obtiene el nombre de usuario."""
        self.assertEqual(str(self.user.user_location), 'test_user')

    def test_location_string(self):
        """Si se añaden los campos de localización, location_string
        sera el valor de la concatenación de todos ellos.
        """
        self.user.user_location.country = 'España'
        self.user.user_location.state = 'Barcelona'
        self.user.user_location.city = 'Granollers'
        self.user.user_location.address = 'Ramon Llull 28'
        self.user.user_location.zipcode = '08401'
        self.user.user_location.save()
        user = UserModel.objects.get(pk=self.user.pk)
        location_string = '{}, {}, {}, {}, {}'.format(
            self.user.user_location.country,
            self.user.user_location.state,
            self.user.user_location.city,
            self.user.user_location.address,
            self.user.user_location.zipcode
        )

        self.assertEqual(user.user_location.location_string, location_string)


class UserOptionsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user = UserModel.objects.create_user(
            username='test_user',
            password='123',
            email='test_user@example.com'
        )

    def test_opciones_por_defecto(self):
        """Todas las opciones del usuario."""
        self.assertFalse(self.user.user_options.phone_public)
        self.assertFalse(self.user.user_options.address_public)
        self.assertFalse(self.user.user_options.email_public)
        self.assertTrue(self.user.user_options.notify_precio_anuncio_baja)

    def test_str(self):
        """Obtiene el nombre de usuario."""
        self.assertEqual(str(self.user.user_options), 'test_user')
