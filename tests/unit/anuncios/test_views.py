from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse

from anuncios import settings as anuncios_settings
from anuncios.models import AnuncioHabitacion

from .base_anuncios import BaseAnuncioTest


class AnuncioListViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:list'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_status_code_200_solo_superuser(self):
        """Solo el superuser tiene acceso a la lista de anuncios."""
        self.assertEqual(self.response.status_code, 200)

        # Usuario anónimo
        self.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

        # Usuario normal
        self.login('perico', '123')
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/list.html')

    def test_context_object_name(self):
        """Comprueba que anuncios este en contexto y tenga items."""
        self.assertIn('anuncios', self.response.context)
        self.assertGreater(self.response.context['anuncios'].count(), 0)

    def test_pagination_num(self):
        """Numero de anuncios es igual al de anuncios.settings.ANUNCIO_PAGINATE_BY."""
        self.assertEqual(
            self.response.context['anuncios'].count(),
            anuncios_settings.ANUNCIO_PAGINATE_BY
        )


class AnuncioListByOwnerViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:list_by_owner'
        self.url = reverse(self.urlconf, kwargs={'slug': 'perico'})
        self.login()
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        """Solo el superuser tiene acceso a la lista de anuncios."""
        self.assertEqual(self.response.status_code, 200)

    def test_si_no_existe_slug_usuario_lanzara_404(self):
        """Si slug de usuario no existe, lanzara Http404."""
        response = self.client.get(reverse(self.urlconf, kwargs={'slug': 'noexisto'}))

        self.assertEqual(response.status_code, 404)

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/list_owner.html')
        self.assertTemplateUsed(self.response, 'anuncios/_anuncio_list.html')
        self.assertTemplateUsed(self.response, 'anuncios/_anuncio_caracteristicas_card.html')
        self.assertTemplateUsed(self.response, 'favorites/_heart_favorites.html')

    def test_get_context_data(self):
        """Comprueba variables de contexto."""
        context = self.response.context

        # Variable owner
        self.assertIn('owner', context)

        # owner es perico.
        self.assertEqual(context['owner'].username, 'perico')

    def test_get_queryset(self):
        """Si el usuario es el owner de los anuncios, le mostrara los anuncios
        active=False.
        """
        self.logout()
        self.anuncio_model.objects.filter(owner=2).update(active=False)
        self.login('perico', '123')
        anuncios = self.client.get(self.url).context['anuncios']

        self.assertGreater(anuncios.count(), 1)

    def test_opciones_de_owner(self):
        """Si el usuario es el owner del anuncio, le da opciones de editar
        imágenes del anuncio y activar/desactivar el anuncio.

        IMPORTANTE: data-original-title es por que en el elemento se pone
        title="", si se cambia a data-title="", data-original-title estará vació.
        """
        # TODO: Por mas vueltas que le doy, no consigo que funcione.
        # assertContains no puede probar nada que este en un {% include 'template.html' %}

        # # Si no es owner, no le mostrara las opciones.
        # self.assertEqual(self.response.context['user'].username, 'snicoper')
        # self.assertNotContains(self.response, 'data-original-title="Editar anuncio"')
        # self.assertNotContains(self.response, 'data-original-title="Editar imágenes"')
        # self.assertNotContains(self.response, 'data-original-title="Activo / Desactivar"')
        #
        # # Si es owner, si tendrá las opciones de edición.
        # self.login('perico', '123')
        # response = self.client.get('/anuncios/perico/list/')
        # self.assertEqual(response.context['user'].username, 'perico')
        # self.assertContains(response, 'data-original-title="Editar anuncio"')
        # self.assertContains(response, 'data-original-title="Editar imágenes"')
        # self.assertContains(response, 'data-original-title="Activo / Desactivar"')

    def test_anuncios_de_snicoper_no_los_muestra(self):
        """Ningun anuncio mostrado pertenece a snicoper."""
        anuncio_list = self.response.context['anuncios']
        owner = self.user_model.objects.get(slug='perico')
        for anuncio in anuncio_list:
            self.assertEqual(anuncio.owner, owner)


class AnuncioDetailViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:details'
        self.url = reverse(self.urlconf, kwargs={'pk': 1})
        self.login()
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        """Prueba el status_code."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/details.html')

    def test_si_esta_inactive_solo_owner_puede_verlo(self):
        """Si el anuncio esta inactivo, solo el owner puede verlo."""
        self.logout()
        anuncio = self.anuncio_model.objects.filter(owner=self.user).first()
        anuncio.active = False
        anuncio.save()

        # Usuario anónimo, Http404
        response = self.client.get(reverse(self.urlconf, kwargs={'pk': anuncio.id}))

        self.assertEqual(response.status_code, 404)

        # Usuario logueado pero no owner, Http404
        self.login('perico', '123')
        response = self.client.get(reverse(self.urlconf, kwargs={'pk': anuncio.id}))

        self.assertEqual(response.status_code, 404)

        # Owner si status_code 200
        self.logout()
        self.login()
        response = self.client.get(reverse(self.urlconf, kwargs={'pk': anuncio.id}))

        self.assertEqual(response.status_code, 200)

    def test_context_object_name(self):
        """Context object name, anuncio."""
        self.assertIn('anuncio', self.response.context)

    def test_get_context_data(self):
        """Requiere del form para crear pmessages."""
        context = self.response.context
        anuncio = context['anuncio']
        user = context['user']

        self.assertIn('form', context)

        # Comprobar los datos iniciales.
        initial = context['form'].initial
        self.assertEqual(initial['anuncio'], anuncio)
        self.assertEqual(initial['sender'], user)
        self.assertEqual(initial['recipient'], anuncio.owner)

    def test_views_incrementa_en_1(self):
        """Incrementa en 1 cada vez que se ve el anuncio."""
        # Actualmente es 0, incrementa en 1, excepto si el usuario es superuser.
        self.client.get(reverse(self.urlconf, kwargs={'pk': 1}))
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertEqual(anuncio.views, 0)

        self.login('perico', '123')
        self.client.get(reverse(self.urlconf, kwargs={'pk': 1}))
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertEqual(anuncio.views, 1)

        # Incrementa en 1.
        self.client.get(reverse(self.urlconf, kwargs={'pk': 1}))
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertEqual(anuncio.views, 2)

    def test_campo_update_at(self):
        """Actualiza el campo update_at.

        Las reglas para poderlo actualizar son: que el anuncio sea premium y
        solo una vez cada ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT días.

        Para probarlos con HTML, se comprobara el material icon ya que es único
        en la pagina y con el color de texto, lo hace único según "permisos".

        Puede actualizar: <i class="material-icons green-text">update</i>
        Es premium pero no puede actualizar: <i class="material-icons orange-text">update</i>
        No es premium: <i class="material-icons red-text">update</i>

        También prueba la view 'src/apps/anuncios/api.py'.
        """
        # Ahora el anuncio, no es premium, por lo tanto red-text.
        self.assertContains(self.response, '<i class="material-icons text-danger">update</i>')

        # Actualizar el anuncio a premium y mostrara green-text.
        anuncio = self.anuncio_model.objects.get(pk=1)

        anuncio.is_premium = True
        anuncio.save()
        response = self.client.get(self.url)

        self.assertContains(response, '<i class="material-icons text-success">update</i>')

        # Ahora al obtener de nuevo la pagina, mostrara el orange-text.
        self.client.post(
            reverse('anuncios:api_update_at', kwargs={'anuncio_id': '1'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = self.client.get(self.url)

        self.assertContains(response, '<i class="material-icons text-warning">update</i>')

    def test_anuncio_id_8_habitacion(self):
        """El Anuncio ID 8 es una habitacion y el genero es para CHICA."""
        response = self.client.get(reverse(self.urlconf, kwargs={'pk': 8}))

        self.assertContains(response, 'Chicas')

    def test_anuncio_id_12_habitacion(self):
        """El Anuncio ID 8 es una habitacion y el genero es para CHICO."""
        response = self.client.get(reverse(self.urlconf, kwargs={'pk': 12}))

        self.assertContains(response, 'Chicos')


class AnuncioCreateSelectListViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:create_select'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        """Prueba el status_code."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/create_select_list.html')

    def test_get_context_data(self):
        """Comprueba variables de contexto."""
        context = self.response.context

        # Variable owner
        self.assertIn('category_list', context)

        # Es un diccionario
        self.assertIsInstance(self.response.context['category_list'], dict)


class AnuncioCreateViewTest(BaseAnuncioTest):
    """La reglas de creación de un anuncio es simple, un mismo usuario solo
    puede tener un máximo de 3 anuncios gratuitos, pero no cuentan los anuncios
    premium.
    """

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:create'
        self.url = reverse(
            self.urlconf,
            kwargs={'category': self.anuncio_model.HABITACION.lower()}
        )
        self.login()
        self.response = self.client.get(self.url)
        self.form_data = {
            "country": "Espa\u00f1a",
            "state": "Barcelona",
            "city": "Granollers",
            "address": "Ramon Llull 28 1\u00ba 1\u00ba",
            "zipcode": "08401",
            "owner": 2,
            "category": "HABITACION",
            "metros_cuadrados": None,
            "phone": "987654321",
            "precio": "200",
            "type_anuncio": "ALQUILER",
            "genero": "CHICOCHICA",
            "permite_fumar_piso": False,
            "permite_fumar_habitacion": True,
            "internet": False,
            "description": "",
            "is_premium": False,
            "latitude": 41.6140513,
            "longitude": 2.28780340000003
        }

    def test_status_code_200_usuario_login(self):
        """Prueba el status_code."""
        self.assertEqual(self.response.status_code, 200)

        # Usuario anónimo Http404
        self.logout()
        response = self.client.get(self.url, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            reverse(self.urlconf, kwargs={'category': self.anuncio_model.HABITACION.lower()})
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/form.html')

    def test_ANUNCIO_MAX_ANUNCIOS(self):
        """Prueba varios casos con ANUNCIO_MAX_ANUNCIOS.

        Un usuario puede tener un máximo de ANUNCIO_MAX_ANUNCIOS anuncios gratis.

        Si tiene 40 anuncios premium y ninguno gratis, aun podrá crear los
        ANUNCIO_MAX_ANUNCIOS anuncios gratis.
        """
        new_user = self.user_model.objects.create_user(
            username='palote',
            email='palote@example.com',
            password='123456'
        )
        # Superuser puede poner todos los que quiera.
        self.assertEqual(self.response.status_code, 200)

        self.logout()
        self.login(new_user.username, '123456')

        # El usuario no tiene ningún anuncio, por lo tanto le muestra el form.
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Usuario crea ANUNCIO_MAX_ANUNCIOS y ya no podrá poner mas anuncios.
        form_data = self.form_data.copy()
        form_data['owner'] = new_user.pk
        for i in range(0, anuncios_settings.ANUNCIO_MAX_ANUNCIOS):
            self.client.post(self.url, data=form_data)

        new_user_anuncios_count = self.anuncio_model.objects.filter(owner=new_user).count()
        self.assertEqual(new_user_anuncios_count, anuncios_settings.ANUNCIO_MAX_ANUNCIOS)
        response = self.client.get(self.url, follow=True)
        expected_url = reverse('payments:process_anuncio_premium')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Si un anuncio se convierte en premium, new_user podrá crear un anuncio gratis mas.
        anuncio = self.anuncio_model.objects.filter(owner=new_user).first()
        anuncio.is_premium = True
        anuncio.save()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        """Comprueba variables de contexto."""
        context = self.response.context

        self.assertIn('title', context)
        self.assertIn('btn_form_name', context)
        self.assertIn('category_name', context)

    def test_get_initial(self):
        """Comprueba los initial del form.

        NOTA: No entiendo por que antes de cada self.client.get(self.url)
        he de poner self.login().
        """
        initial = self.response.context['form'].initial

        # category
        self.assertIn('category', initial)
        self.assertEqual(initial['category'], self.anuncio_model.HABITACION)

        # owner
        self.assertIn('owner', initial)
        self.assertEqual(initial['owner'], self.user.id)

        # phone solo lo muestra si lo tiene y además es público.
        self.assertNotIn('phone', initial)

        self.user.phone = '123123'
        self.user.user_options.phone_public = True
        self.user.user_options.save()
        self.user.save()
        self.login()
        response = self.client.get(self.url)
        initial = response.context['form'].initial

        self.assertIn('phone', initial)
        self.assertEqual(initial['phone'], '123123')

        # is_premium, por defecto no lo muestra.
        self.assertNotIn('is_premium', initial)

        self.user.is_premium = True
        self.user.save()
        self.login()
        response = self.client.get(self.url)
        initial = response.context['form'].initial

        self.assertEqual(initial['is_premium'], True)

        # Al ser un anuncio para HABITACION, tendra el genero en CHICOCHICA.
        self.assertContains(response, AnuncioHabitacion.CHICOCHICA)

        # Localización depende de si el usuario la tiene en user_location.
        self.assertNotIn('country', initial)
        self.assertNotIn('state', initial)
        self.assertNotIn('city', initial)

        self.user.user_location.country = 'España'
        self.user.user_location.state = 'Barcelona'
        self.user.user_location.city = 'Granollers'

        # Verifica la latitude para saver si tiene puesta una Localización.
        self.user.user_location.latitude = '123123'
        self.user.user_location.save()
        self.login()
        response = self.client.get(self.url)
        initial = response.context['form'].initial

        self.assertIn('country', initial)
        self.assertIn('state', initial)
        self.assertIn('city', initial)

        self.assertEqual(initial['country'], 'España')
        self.assertEqual(initial['state'], 'Barcelona')
        self.assertEqual(initial['city'], 'Granollers')

    def test_post(self):
        """Test de la creación de una anuncio.

        Para que pase el test, requiere de que snicoper tenga una
        alerta de habitación en ramon llull en los fixtures.

        La data de este form, lo ha de crear perico, es una habitación.
        """
        # Snicoper como user premium para evitar problemas.
        user = self.user_model.objects.get(pk=2)
        user.is_premium = True
        user.save()
        self.logout()
        self.login(user.username, '123')

        # Crear un anuncio nuevo.
        response = self.client.post(self.url, data=self.form_data, follow=True)
        last_id = self.anuncio_model.objects.order_by('id').last().id
        expected_url = reverse('gallery:image_anuncio_add', kwargs={'id_anuncio': last_id})

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Comprobar que se le ha mandado un Email a snicoper sobre la alerta.
        current_site = Site.objects.get(pk=1)
        subject = 'Anuncio que puede interesarte desde {}'.format(current_site.name)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)

    def test_anuncios_premium_decrementa_en_1(self):
        """Cuando el anuncio se crea, si es de user.anuncios_premium,
        al crearlo se ha de decrementar en 1."""
        perico = self.user_model.objects.get(pk=1)
        perico.increase_anuncio()
        perico.save()

        self.assertEqual(perico.anuncios_premium, 1)

        self.client.post(self.url, data=self.form_data)
        perico = self.user_model.objects.get(pk=1)

        self.assertEqual(perico.anuncios_premium, 0)


class AnuncioUpdateViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:update'
        self.category = self.anuncio_model.objects.published(owner__id=1).last().category.lower()
        self.url = reverse(self.urlconf, kwargs={'category': self.category, 'pk': 1})
        self.login()
        self.response = self.client.get(self.url)

    def test_status_codes(self):
        """Prueba el status_code."""
        self.assertEqual(self.response.status_code, 200)

        # Usuario anónimo Http404
        self.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        # Un usuario no puede editar los anuncios de otro usuario.
        self.login('perico', '123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_template_usado(self):
        """Comprueba el template."""
        self.assertTemplateUsed(self.response, 'anuncios/form.html')

    def test_get_context_data(self):
        """Comprueba variables de contexto."""
        context = self.response.context

        self.assertIn('btn_form_name', context)
        self.assertEqual(context['btn_form_name'], 'Actualizar')

        self.assertIn('title', context)
        self.assertEqual(context['title'], 'Actualizar Anuncio')

    def test_post(self):
        """Comprobaciones para actualizar un anuncio."""
        initial = self.response.context['form'].initial
        initial_copy = initial
        initial_copy['precio'] = '111111'

        response = self.client.post(self.url, data=initial_copy, follow=True)
        expected_url = reverse('anuncios:details', kwargs={'pk': 1})

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # El valor ha cambiado.
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertEqual(anuncio.precio, 111111)


class AnuncioDeactivateViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:deactivate'
        self.url = reverse(self.urlconf, kwargs={'id_anuncio': 1})
        self.login()
        self.response = self.client.get(self.url)

    def test_status_code_200_solo_superuser(self):
        """Solo el superuser tiene acceso a la lista de anuncios."""
        self.assertEqual(self.response.status_code, 302)

        # Usuario anónimo
        self.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

        # Usuario normal
        self.login('perico', '123')
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_desactiva_anuncio(self):
        """Desactiva correctamente un anuncio."""
        # Por defecto setUp lo desactiva, buscamos otro.
        anuncio = self.anuncio_model.objects.filter(owner__id=1).first()

        self.assertTrue(anuncio.active)

        response = self.client.get(reverse(self.urlconf, kwargs={'id_anuncio': anuncio.pk}))

        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': anuncio.pk}),
            status_code=302,
            target_status_code=200
        )

        anuncio = self.anuncio_model.objects.get(pk=anuncio.pk)

        self.assertFalse(anuncio.active)


class AnuncioActivateViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:activate'
        self.user_snicoper = self.user_model.objects.get(pk=1)
        self.user_perico = self.user_model.objects.get(pk=2)
        self.anuncio_snicoper = self.anuncio_model.objects.filter(owner=self.user_snicoper).first()
        self.anuncio_perico = self.anuncio_model.objects.filter(owner=self.user_perico).first()

    def test_status_code(self):
        """Solo usuario owner del anuncio puede acceder al anuncio."""
        # Snicoper tiene acceso para desactivar su propio anuncio.
        # Redireccionara de nuevo al anuncio.
        self.login(self.user_snicoper.username, '123')
        response = self.client.get(
            reverse(self.urlconf, kwargs={'id_anuncio': self.anuncio_snicoper.pk})
        )

        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': self.anuncio_snicoper.pk}),
            status_code=302,
            target_status_code=200
        )

        # Perico no tiene acceso para activar un anuncio de snicoper.
        self.logout()
        self.login(self.user_perico.username, '123')
        response = self.client.get(
            reverse(self.urlconf, kwargs={'id_anuncio': self.anuncio_snicoper.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_activar_anuncio_sin_ser_account_premium(self):
        """Si tiene el limite de anuncios y no es premium el anuncio,
        redirecciona a la pagina de comprar anuncio premium.

        Lo que cuenta no es la cantidad de anuncios que tenga, si no la cantidad
        de anuncios normales activos.
        """
        new_user = self.user_model.objects.create_user(
            username='palote',
            email='palote@example.com',
            password='123456'
        )
        form_data = {
            "country": "Espa\u00f1a",
            "state": "Barcelona",
            "city": "Granollers",
            "address": "Ramon Llull 28 1\u00ba 1\u00ba",
            "zipcode": "08401",
            "owner": new_user.pk,
            "category": "HABITACION",
            "metros_cuadrados": None,
            "phone": "987654321",
            "precio": "200",
            "type_anuncio": "ALQUILER",
            "genero": "CHICOCHICA",
            "permite_fumar_piso": False,
            "permite_fumar_habitacion": True,
            "internet": False,
            "description": "",
            "is_premium": False,
            "active": False,
            "latitude": 41.6140513,
            "longitude": 2.28780340000003
        }
        url = reverse(
            'anuncios:create',
            kwargs={'category': self.anuncio_model.HABITACION.lower()}
        )
        self.logout()
        self.login(new_user.username, '123456')

        # Crear anuncios via POST.
        for i in range(0, anuncios_settings.ANUNCIO_MAX_ANUNCIOS):
            self.client.post(url, data=form_data)

        new_user_anuncios_list = self.anuncio_model.objects.filter(owner=new_user)
        self.assertEqual(new_user_anuncios_list.count(), anuncios_settings.ANUNCIO_MAX_ANUNCIOS)

        # Puede activar los 3 anuncios.
        for anuncio in new_user_anuncios_list:
            response = self.client.get(reverse(self.urlconf, kwargs={'id_anuncio': anuncio.pk}))

            # Redirecciona a detalles del anuncios
            self.assertRedirects(
                response=response,
                expected_url=reverse('anuncios:details', kwargs={'pk': anuncio.pk}),
                status_code=302,
                target_status_code=200
            )

        # Un anuncio ya creado, poner como owner a new_user y ponerlo como active=False.
        new_anuncio = self.anuncio_model.objects.get(pk=1)
        new_anuncio.owner = new_user
        new_anuncio.active = False
        new_anuncio.save()

        # Si ahora se intenta activar, no dejara.
        response = self.client.get(reverse(self.urlconf, kwargs={'id_anuncio': new_anuncio.pk}))

        # Redirecciona a payments.
        self.assertRedirects(
            response=response,
            expected_url=reverse('payments:process_anuncio_premium'),
            status_code=302,
            target_status_code=200
        )

        # El primer anuncio de new_user, convertirlo a premium.
        first = self.anuncio_model.objects.filter(
            owner=new_user
        ).exclude(pk=new_anuncio.pk).first()
        first.is_premium = True
        first.save()

        # Esta desactivado.
        self.assertFalse(self.anuncio_model.objects.get(pk=new_anuncio.pk).active)

        # Intentar activar new_anuncio, que si debería.
        response = self.client.get(reverse(self.urlconf, kwargs={'id_anuncio': new_anuncio.pk}))

        # Esta activo.
        self.assertTrue(self.anuncio_model.objects.get(pk=new_anuncio.pk).active)

        # Redirecciona a detalles del anuncios
        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': new_anuncio.pk}),
            status_code=302,
            target_status_code=200
        )

    def test_activar_anuncio_siendo_cuenta_premium(self):
        """Un usuario Premium puede activar los anuncios."""
        self.anuncio_snicoper.active = False
        self.anuncio_snicoper.save()
        self.user_snicoper.is_premium = True
        self.user_snicoper.save()
        self.login(self.user_snicoper.username, '123')
        response = self.client.get(
            reverse(self.urlconf, kwargs={'id_anuncio': self.anuncio_snicoper.pk}),
            follow=True
        )

        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': self.anuncio_snicoper.pk}),
            status_code=302,
            target_status_code=200
        )
        anuncio = self.anuncio_model.objects.get(pk=self.anuncio_snicoper.pk)

        self.assertTrue(anuncio.active)

    def test_anuncio_premium_se_puede_activar(self):
        """Si un anuncio es Premium, se puede activar sin importar que sea
        anuncios Premium o cuenta Premium.
        """
        self.anuncio_snicoper.active = False
        self.anuncio_snicoper.is_premium = True
        self.anuncio_snicoper.save()
        self.login(self.user_snicoper.username, '123')
        response = self.client.get(
            reverse(self.urlconf, kwargs={'id_anuncio': self.anuncio_snicoper.pk}),
            follow=True
        )

        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': self.anuncio_snicoper.pk}),
            status_code=302,
            target_status_code=200
        )
        anuncio = self.anuncio_model.objects.get(pk=self.anuncio_snicoper.pk)

        self.assertTrue(anuncio.active)


class AnuncioConvertPremiumViewTest(BaseAnuncioTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'anuncios:convert_anuncio_premium'
        self.url = reverse(self.urlconf, kwargs={'id_anuncio': 1})
        self.form_data = {'can_activate': '1'}
        self.login()

    def test_status_code_get(self):
        """Por method GET redirecciona a payments."""
        # Usuario anónimo Http404
        self.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        # Usuario logueado, sin ser su anuncio Http404.
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        # Usuario logueado con permisos sin ser Premium ni tener anuncios_premium
        # ni el anuncio es Premium, redirecciona para comprar un anuncio.
        self.logout()
        self.login()
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('payments:process_anuncio_premium'),
            status_code=302,
            target_status_code=200
        )

    def test_post_sin_campo_can_activate_redirecciona_al_anuncio(self):
        """Sin can_activate, redirecciona en silencio, pero no convierte en
        anuncio en Premium.
        """
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertFalse(anuncio.is_premium)
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': 1}),
            status_code=302,
            target_status_code=200
        )
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertFalse(anuncio.is_premium)

    def test_si_el_anuncio_ya_es_premium_redirecciona(self):
        """Si un anuncio ya es Premium redirecciona al anuncio en silencio."""
        anuncio = self.anuncio_model.objects.get(pk=1)
        anuncio.is_premium = True
        anuncio.save()

        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertRedirects(
            response=response,
            expected_url=reverse('anuncios:details', kwargs={'pk': 1}),
            status_code=302,
            target_status_code=200
        )
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertTrue(anuncio.is_premium)

    def test_usuario_normal_no_puede_convertir_anuncio_a_premium(self):
        """Un usuario no puede convertir el anuncio a Premium, por no ser ningún
        tipo de Premium.
        Redirecciona en silencio.
        """
        self.client.get(self.url, data=self.form_data)
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertFalse(anuncio.is_premium)

    def test_usuario_cuanta_premium(self):
        """Un usuario con cuenta Premium, puede convertirlo a Premium."""
        user = self.user_model.objects.get(pk=1)
        user.is_premium = True
        user.save()
        self.client.post(self.url, data=self.form_data)
        anuncio = self.anuncio_model.objects.get(pk=1)

        self.assertTrue(anuncio.is_premium)

    def test_usuario_con_anuncios_premium(self):
        """Un usuario con anuncios_premium puede convertirlo, pero le descontara
        en 1 los anuncios_premium.
        """
        user = self.user_model.objects.get(pk=1)
        user.anuncios_premium = 1
        user.save()
        self.client.post(self.url, data=self.form_data)
        anuncio = self.anuncio_model.objects.get(pk=1)
        user = self.user_model.objects.get(pk=1)

        self.assertTrue(anuncio.is_premium)
        self.assertEqual(user.anuncios_premium, 0)

    def test_usuario_premium_y_con_anuncios_premium(self):
        """Si un usuario tiene anuncios_premium pero también es cuenta Premium,
        el anuncio se convierte a Premium, pero no descuenta en 1 anuncios_premium.
        """
        user = self.user_model.objects.get(pk=1)
        user.anuncios_premium = 1
        user.is_premium = True
        user.save()
        self.client.post(self.url, data=self.form_data)
        anuncio = self.anuncio_model.objects.get(pk=1)
        user = self.user_model.objects.get(pk=1)

        self.assertTrue(anuncio.is_premium)
        self.assertEqual(user.anuncios_premium, 1)
