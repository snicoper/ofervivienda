from django.core import mail
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils import timezone

from anuncios.models import AnuncioHabitacion, AnuncioPiso
from gallery import settings as gallery_settings
from gallery.models import ImageAnuncio

from .base_anuncios import BaseAnuncioTest


class AnuncioManagerTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()

    def test_published_solo_muestra_los_actives(self):
        """Solo obtendrá los actives = True."""
        old_active = self.anuncio_model.objects.published().count()
        self.anuncio_model.objects.published().\
            filter(id__lte=4).update(active=False)
        new_active = self.anuncio_model.objects.published().count()

        self.assertGreater(old_active, new_active)


class AnuncioTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.PISO,
            'type_anuncio': self.anuncio_model.VENTA,
            'precio': 1000
        }
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)

    def test_owner_es_requerido(self):
        """Campo owner es requerido."""
        with self.assertRaises(IntegrityError):
            self.anuncio_data['owner'] = None
            anuncio = self.anuncio_model.objects.create(**self.anuncio_data)
            self.assertTrue(anuncio)

    def test_category_es_requerido(self):
        """Campo category es requerido."""
        with self.assertRaises(IntegrityError):
            self.anuncio_data['category'] = None
            anuncio = self.anuncio_model.objects.create(**self.anuncio_data)
            self.assertTrue(anuncio)

    def test_type_anuncio_es_requerido(self):
        """Campo type_anuncio es requerido."""
        with self.assertRaises(IntegrityError):
            self.anuncio_data['type_anuncio'] = None
            anuncio = self.anuncio_model.objects.create(**self.anuncio_data)
            self.assertTrue(anuncio)

    def test_currency_default(self):
        """Por defecto currency es EUR."""
        anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

        self.assertEqual(anuncio.currency, self.anuncio_model.EUR)

    def test_premium(self):
        """Por defecto es False."""
        self.assertFalse(self.anuncio.is_premium)

    def test_views_0(self):
        """La propiedad views se pone en 0 al crear un anuncio."""
        anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

        self.assertEqual(anuncio.views, 0)

    def test_update_at_no_actualiza(self):
        """La fecha de update_at se añade al crear, pero no se actualiza sola.

        Para actualizarse se ha de hacer explícitamente.
        """
        old_update_at = self.anuncio.update_at
        anuncio_id = self.anuncio.id
        self.anuncio.category = self.anuncio_model.HABITACION
        self.anuncio.save()
        anuncio = self.anuncio_model.objects.get(pk=anuncio_id)

        self.assertEqual(anuncio.update_at, old_update_at)

    def test_update_at_explicito_cambia_el_orden_queryset(self):
        """Al cambiar el update_at, se pone primero en la lista."""
        old_first_anuncio = self.anuncio_model.objects.first()
        old_last_anuncio = self.anuncio_model.objects.last()
        old_last_anuncio.update_at = timezone.now()
        old_last_anuncio.save()
        new_first_anuncio = self.anuncio_model.objects.first()

        # Ahora old_first_anuncio no es igual a new_first_anuncio
        self.assertNotEqual(old_first_anuncio, new_first_anuncio)

        # Pero si old_last_anuncio es igual a new_first_anuncio
        self.assertEqual(old_last_anuncio, new_first_anuncio)

        # old_first_anuncio ha pasado al 2 item anuncios[1].
        new_second_anuncio = self.anuncio_model.objects.all()[1]

        self.assertEqual(new_second_anuncio, old_first_anuncio)

    def test_str(self):
        """Obtener el location_string."""
        anuncio = self.anuncio_model.objects.get(pk=1)
        expected_title = '{} en {}: {}'.format(
            anuncio.get_category_display(),
            anuncio.get_type_anuncio_display(),
            anuncio.location_string
        )
        self.assertEqual(expected_title, str(anuncio))

    def test_location_string(self):
        """Comprueba que se ha generado location_string."""
        anuncio = self.anuncio_model.objects.get(pk=1)
        location_string = '{}, {}, {}, {}, {}'.format(
            anuncio.country,
            anuncio.state,
            anuncio.city,
            anuncio.address,
            anuncio.zipcode
        )

        self.assertEqual(anuncio.location_string, location_string)

    def test_get_title(self):
        """Prueba obj.get_title."""
        anuncio = self.anuncio_model.objects.get(pk=1)
        expected_title = '{} en {}: {}'.format(
            anuncio.get_category_display(),
            anuncio.get_type_anuncio_display(),
            anuncio.location_string
        )
        self.assertEqual(expected_title, anuncio.get_title)

    def test_get_model_class(self):
        """Obtiene la clase model según la categoría."""
        anuncio_piso = self.anuncio_model.objects.published(
            category=self.anuncio_model.PISO
        )[0]
        anuncio = self.anuncio_model.get_model_class(anuncio_piso.category)

        self.assertIsInstance(anuncio.objects.first(), AnuncioPiso)

    def test_get_absolute_url(self):
        """Prueba model.get_absolute_url."""
        absolute_url = reverse('anuncios:details', kwargs={'pk': self.anuncio.pk})

        self.assertEqual(self.anuncio.get_absolute_url(), absolute_url)

    def test_get_random_thumbnail(self):
        """Prueba los random thumbnail.

        Si tiene mostrara uno al azar, en caso contrario,
        mostrara la imagen por defecto.

        NOTA: este test depende mucho de los fixtures, si
        no hay ninguna imagen en los fixtures dará error.
        """
        media_url = self.test_settings.MEDIA_URL + '{}'

        # Probar un anuncio sin imágenes.
        image = self.anuncio.get_random_thumbnail

        self.assertEqual(
            media_url.format(gallery_settings.GALLERY_THUMBNAIL_DEFAULT),
            image
        )

        # Probar una con images.
        anuncio_id = ImageAnuncio.objects.first().anuncio.pk
        anuncio = self.anuncio_model.objects.get(pk=anuncio_id)

        for i in range(0, 5):
            image = anuncio.get_random_thumbnail
            self.assertNotEqual(
                media_url.format(gallery_settings.GALLERY_THUMBNAIL_DEFAULT),
                image
            )

    def test_precio_anuncio_notifica_si_baja(self):
        """Los usuarios que tienen un anuncio en favoritos, cuando baja el precio
        del anuncio al guardarlos notifica de que ha bajado.

        Da igual si quien lo baja es el owner del anuncio.
        """
        # Por defecto todos los usuarios tienen UserOptions.notify_precio_anuncio_baja en True.
        user = self.user_model.objects.get(pk=1)
        user.favorites_user.anuncios.add(self.anuncio)

        self.assertEqual(user.favorites_user.anuncios.count(), 1)

        # Si incrementa no notifica.
        self.anuncio.precio = self.anuncio.precio + 1
        self.anuncio.save()

        self.assertEqual(len(mail.outbox), 0)

        # Si no cambia no notifica.
        self.anuncio.is_premium = True
        self.anuncio.save()

        self.assertEqual(len(mail.outbox), 0)

        # Si se pone el mismo no notifica.
        self.anuncio.precio = self.anuncio.precio + 1
        self.anuncio.save()

        self.assertEqual(len(mail.outbox), 0)

        # Si baja el precio notifica.
        self.anuncio.precio = self.anuncio.precio - 1
        self.anuncio.save()

        self.assertEqual(len(mail.outbox), 1)


class AnuncioPisoTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.PISO,
            'type_anuncio': self.anuncio_model.VENTA,
            'habitaciones': 4,
            'banos': 2
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.PISO
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)

    def test_anuncio_habitaciones_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['habitaciones'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_banos_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['banos'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)


class AnuncioCasaTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.CASA,
            'type_anuncio': self.anuncio_model.VENTA,
            'habitaciones': 4,
            'banos': 2
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.CASA
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)

    def test_anuncio_habitaciones_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['habitaciones'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_banos_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['banos'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)


class AnuncioApartamentoTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.APARTAMENTO,
            'type_anuncio': self.anuncio_model.VENTA,
            'habitaciones': 4,
            'banos': 2
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.APARTAMENTO
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)

    def test_anuncio_habitaciones_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['habitaciones'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_banos_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['banos'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)


class AnuncioHabitacionTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.HABITACION,
            'genero': AnuncioHabitacion.CHICOCHICA,
            'permite_fumar_piso': True,
            'permite_fumar_habitacion': False,
            'internet': False
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.HABITACION
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)

    def test_anuncio_permite_fumar_piso_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['permite_fumar_piso'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_permite_fumar_habitacion_requerido(self):
        """Intenta crear un anuncio sin campos requeridos."""
        self.anuncio_data['permite_fumar_habitacion'] = None

        with self.assertRaises(IntegrityError):
            self.anuncio_model.objects.create(**self.anuncio_data)

    def test_default_de_genero_es_indiferente(self):
        """Por defecto el campo genero es AnuncioHabitacion.CHICOCHICA."""
        anuncio_data = self.anuncio_data.copy()
        del anuncio_data['genero']
        anuncio = self.anuncio_model.objects.create(**anuncio_data)

        self.assertEqual(anuncio.genero, AnuncioHabitacion.CHICOCHICA)

    def test_cuando_guarda_establece_type_anuncio_en_ALQUILER(self):
        """Cuando una habitación se crea, type_anuncio se guarda como ALQUILER."""
        self.assertEqual(self.anuncio.type_anuncio, self.anuncio_model.ALQUILER)


class AnuncioTerrenoTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.TERRENO,
            'type_anuncio': self.anuncio_model.ALQUILER
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.TERRENO
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)


class AnuncioParkingTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.PARKING,
            'type_anuncio': self.anuncio_model.ALQUILER
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.PARKING
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)


class AnuncioIndustrialTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.INDUSTRIAL,
            'type_anuncio': self.anuncio_model.ALQUILER
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.INDUSTRIAL
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)


class AnuncioLocalTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.anuncio_data = {
            'owner': self.user,
            'category': self.anuncio_model.LOCAL,
            'type_anuncio': self.anuncio_model.ALQUILER
        }
        self.anuncio_model = self.anuncio_model.get_model_class(
            self.anuncio_model.LOCAL
        )
        self.anuncio = self.anuncio_model.objects.create(**self.anuncio_data)

    def test_anuncio_es_creado(self):
        """Crea un anuncio con los datos mínimos."""
        self.assertTrue(self.anuncio)
