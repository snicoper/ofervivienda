from django.urls import reverse

from .base_anuncios import BaseAnuncioTest


class AnuncioUploadUpdateAtApiViewTest(BaseAnuncioTest):

    def setUp(self):
        """Es necesario hacer el anuncio premium para las pruebas.

        Aquí no prueba las reglas para actualizar un anuncio, solo la api.
        """
        super().setUp()
        self.anuncio = self.anuncio_model.objects.filter(owner=self.user).first()
        self.anuncio.is_premium = True
        self.anuncio.save()
        self.urlconf = 'anuncios:api_update_at'
        self.url = reverse(self.urlconf, kwargs={'anuncio_id': self.anuncio.id})
        self.login()
        self.response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_no_ajax_return_BAD(self):
        """Si no es via aja, Http404."""
        response = self.client.post(self.url)
        self.assertContains(response, 'BAD')

    def test_usuario_logout_redirecciona(self):
        """Un usuario anónimo lo redirecciona."""
        self.logout()
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_anuncio_no_existe_return_BAD(self):
        """Si se intenta actualizar un anuncio que no existe, retorna BAD."""
        url = reverse(self.urlconf, kwargs={'anuncio_id': 1000})
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'BAD')

    def test_anuncio_no_es_de_owner_return_BAD(self):
        """Prueba que el usuario que actualiza, sea el owner del anuncio."""
        self.login('perico', '123')
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'BAD')

    def test_todo_OK(self):
        """Prueba un petición OK."""
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'OK')

    def test_get(self):
        """Http via GET devuelve BAD."""
        response = self.client.get(self.url)
        self.assertContains(response, 'BAD')
