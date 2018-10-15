from django.urls import reverse

from authentication.models import RegisterUser

from .base_stats import BaseAdmin2Test


class AdminIndexViewTest(BaseAdmin2Test):

    def setUp(self):
        super().setUp()
        self.urlconf = 'stats:index'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_anonimo_404(self):
        """Un usuario anónimo lanza Http404."""
        self.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_usuario_no_superuser_404(self):
        """Un usuario logueado pero que no sea superuser, le lanza un Http404."""
        self.login('perico', '123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_usuario_superuser_200(self):
        """Un usuario superuser le muestra la pagina."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template_usado."""
        self.assertTemplateUsed(self.response, 'stats/index.html')

    def test_context_data(self):
        """Prueba get_context_data.

        Lo importante es que exista el contexto.
        """
        context = self.response.context

        # Total usuarios.
        self.assertEqual(context['total_usuarios'], 2)

        # Usuarios hoy.
        self.assertEqual(context['usuarios_hoy'], 0)

        # Registrar un nuevo usuario.
        self.user_model.objects.create(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        response = self.client.get(self.url)

        self.assertEqual(response.context['usuarios_hoy'], 1)

        # Registros temporales.
        self.assertEqual(context['registros_temporales'], 0)

        # Registrar un usuario temporal.
        RegisterUser.objects.create(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        response = self.client.get(self.url)

        self.assertEqual(response.context['registros_temporales'], 1)

        # Payments
        self.assertEqual(response.context['total_payment']['receiver_amount__sum'], None)
        self.assertEqual(response.context['total_payment_week']['receiver_amount__sum'], None)
        self.assertEqual(response.context['total_payment_month']['receiver_amount__sum'], None)

        # Pmessages creados.
        self.assertIn('pmessages_creados', context)

        # Alertas creadas.
        self.assertIn('alertas_creadas', context)

        # Total anuncios.
        self.assertEqual(response.context['total_anuncios'], 14)

        # Anuncios activos.
        self.assertEqual(response.context['anuncios_activos'], 14)

        # Anuncios ultima semana.
        self.assertEqual(response.context['anuncios_ultima_semana'], 0)

        # Anuncios hoy.
        self.assertEqual(response.context['anuncios_hoy'], 0)

        # views total anuncios.
        self.assertIn('anuncios_hoy', response.context)
