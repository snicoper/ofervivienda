from django.urls import reverse

from .base_favorites import BaseFavoritesTest


class FavoritesListViewTest(BaseFavoritesTest):

    def setUp(self):
        super().setUp()
        self.anuncios = self.anuncio_model.objects.all()[:5]
        for anuncio in self.anuncios:
            self.user.favorites_user.anuncios.add(anuncio)
        self.url = 'favorites:list'
        self.urlconf = reverse(self.url)
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_usuario_login_status_code_200(self):
        """Solo los usuario con login pueden ver su lista de favoritos."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_anonimo_status_code_302(self):
        """Un usuario anónimo lo redirecciona a pagina de login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.urlconf
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_usuario_sin_favorites(self):
        """Un usuario sin favoritos, muestra el mensaje de que no tiene una
        lista para mostrar.
        """
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)
        mensaje = '<h2>No hay anuncios para mostrar.</h2>'

        self.assertContains(response, mensaje)

    def test_template_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'favorites/favorites_list.html')

    def test_los_anuncios_mostrados_todos_son_favoritos_del_usuario(self):
        """Todos los anuncios mostrados son favoritos del usuario que los
        solicita.
        """
        anuncios = self.response.context['anuncios']

        for anuncio in anuncios:
            favorites = anuncio.favorites_anuncios.all()
            for fav in favorites:
                self.assertEqual(fav.owner, self.user)


class FavoriteUserListDeleteView(BaseFavoritesTest):

    def setUp(self):
        super().setUp()
        self.anuncios = self.anuncio_model.objects.all()[:5]
        for anuncio in self.anuncios:
            self.user.favorites_user.anuncios.add(anuncio)
        self.url = 'favorites:delete_all'
        self.urlconf = reverse(self.url)
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_usuario_login_status_code_200(self):
        """Para usuario con login status_code == 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_anonimo_status_code_302(self):
        """Un usuario anónimo redirecciona a login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(reverse('authentication:login'), self.urlconf)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado_en_method_get(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'favorites/delete_all.html')

    def test_elimina_favoritos_method_post(self):
        """Elimina los favoritos cuando el method es POST."""
        self.assertEqual(self.user.favorites_user.anuncios.count(), 5)
        response = self.client.post(self.urlconf, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('favorites:list'),
            status_code=302,
            target_status_code=200
        )

        # Se han eliminado los favoritos.
        self.assertEqual(self.user.favorites_user.anuncios.count(), 0)


class FavoritesAjaxAddViewTest(BaseFavoritesTest):

    def setUp(self):
        super().setUp()
        self.url = 'favorites:api_add'
        self.urlconf = reverse(self.url)
        self.login()
        self.response = self.client.post(
            self.urlconf,
            {'anuncio_id': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_anadir_favorite_via_ajax(self):
        """Añade el user un favorito a su lista."""
        self.assertEqual(self.user.favorites_user.anuncios.count(), 1)

    def test_si_no_es_ajax_no_permitido(self):
        """Solo se puede acceder a la consulta via AJAX."""
        # method GET 404
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 405)

        # method POST 405
        response = self.client.post(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_si_ya_tiene_anadido_fav_no_lo_añade(self):
        """Si el anuncio ya esta en favorito, no lo vuelve a añadir."""
        self.client.post(
            self.urlconf,
            {'anuncio_id': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(self.user.favorites_user.anuncios.count(), 1)


class FavoritesAjaxRemoveViewTest(BaseFavoritesTest):

    def setUp(self):
        super().setUp()
        self.url = 'favorites:api_remove'
        self.urlconf = reverse(self.url)
        self.login()

    def test_anadir_favorite_via_ajax(self):
        """Añade el user un favorito a su lista."""
        anuncio = self.anuncio_model.objects.get(pk=1)
        self.user.favorites_user.anuncios.add(anuncio)
        self.assertEqual(self.user.favorites_user.anuncios.count(), 1)
        self.response = self.client.post(
            self.urlconf,
            {'anuncio_id': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(self.user.favorites_user.anuncios.count(), 0)

    def test_si_no_es_ajax_no_permitido(self):
        """Solo se puede acceder a la consulta via AJAX."""
        # method GET 404
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 405)

        # method POST 405
        response = self.client.post(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_si_no_tiene_el_fav_no_hace_nada(self):
        """Si el anuncio ya esta en favorito, no lo vuelve a añadir."""
        self.client.post(
            self.urlconf,
            {'anuncio_id': '1'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(self.user.favorites_user.anuncios.count(), 0)
