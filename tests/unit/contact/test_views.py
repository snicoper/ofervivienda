from django.core import mail
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import ContactMessage

from .base_contact import BaseContactTest


class ContactViewTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        self.user = self.user_model.objects.get(pk=1)
        self.url = 'contact:contact'
        self.urlconf = reverse(self.url)
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_status_code_200(self):
        """Tanto un usuario logueado como anónimo obtiene el status_code 200."""
        # Usuario logueado.
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 200)
        self.logout()

        # Usuario anónimo.
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'contact/contact.html')

    def test_form_usado(self):
        """Form usado en la view."""
        form = self.response.context['form']

        self.assertIsInstance(form, ContactForm)

    def test_usuario_login_campos_con_datos(self):
        """Un usuario logueado, tendrá username, email rellenados."""
        initial = self.response.context['form'].initial

        # Campo username.
        self.assertEqual(initial['username'], self.user.username)

        # Campo email.
        self.assertEqual(initial['email'], self.user.email)

    def test_usuario_anonimo_campos_sin_datos(self):
        """Un usuario anónimo, el campo username y email esbaran vacíos.

        Lanza KeyError por que no existe el key en initial.
        """
        self.logout()
        response = self.client.get(self.urlconf)
        initial = response.context['form'].initial

        # Campo username.
        with self.assertRaises(KeyError):
            initial['username']

        # Campo email.
        with self.assertRaises(KeyError):
            initial['email']

    def test_post(self):
        """Un usuario con login, manda el form y abra un email."""
        form_data = {
            'subject': 'Subject test',
            'message': 'Content message',
            'username': self.user.username,
            'email': self.user.email,
            'is_register': True
        }
        self.assertEqual(ContactMessage.objects.count(), 0)
        response = self.client.post(self.urlconf, data=form_data, follow=True)
        expected_url = reverse('home_page')

        # Se ha guardado el mensaje en la db.
        self.assertEqual(ContactMessage.objects.count(), 1)

        # Redirecciona a home.
        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Hay un email en la bandeja de salida.
        self.assertEqual(len(mail.outbox), 1)

        # Campo is_register = True.
        message = ContactMessage.objects.first()

        self.assertTrue(message.is_register)


class ContactMessageListViewTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        self.url = 'contact:message_list'
        self.urlconf = reverse(self.url)
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_status_code(self):
        """Solo el usuario con permisos puede ver la pagina. De lo contrario
        lanza un Http404.
        """
        self.assertEqual(self.response.status_code, 200)

        # Usuario anónimo, lanza Http404.
        self.logout()
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

        # Usuario logueado, pero sin permisos lanza Http404
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_templete_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'contact/message_list.html')

    def test_context_object_name(self):
        """Prueba context_object_name."""
        self.assertIn('message_list', self.response.context)


class ContactMessageDetailViewTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        data = {
            'subject': 'Subject test',
            'message': 'Content message',
            'email': 'testuser@example.com',
            'username': 'testuser',
            'is_register': False
        }
        self.contact = ContactMessage.objects.create(**data)
        self.url = 'contact:message_detail'
        self.urlconf = reverse(self.url, kwargs={'pk': self.contact.pk})
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_status_code(self):
        """Solo el usuario con permisos puede ver la pagina.

        De lo contrario lanza un Http404.
        """
        self.assertEqual(self.response.status_code, 200)

        # Usuario anónimo, lanza Http404.
        self.logout()
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

        # Usuario logueado, pero sin permisos lanza Http404
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_templete_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'contact/message_detail.html')

    def test_context_object_name(self):
        """Prueba context_object_name."""
        self.assertIn('message', self.response.context)

    def test_context_data(self):
        """El mensaje lo marca como leído."""
        message = ContactMessage.objects.get(pk=self.contact.pk)

        self.assertTrue(message.read)
