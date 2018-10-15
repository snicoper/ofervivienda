import os

from django.core import mail
from django.urls import reverse

from pmessages import views

from .base_pmessages import BasePmessagesTest


class MessageInboxViewTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.data = self.load_data(
            os.path.join(os.path.dirname(__file__), 'pmessages_data.json')
        )
        # data requiere de instancias
        self.data['anuncio'] = self.anuncio_model.objects.get(pk=self.data['anuncio'])
        self.data['sender'] = self.user_model.objects.get(pk=self.data['sender'])
        self.data['recipient'] = self.user_model.objects.get(pk=self.data['recipient'])

        self.urlconf = 'pmessages:inbox'
        self.url = reverse(self.urlconf)
        self.login()

        # Crear un usuario nuevo y una alerta nueva.
        self.testuser = self.user_model.objects.create_user(
            username='testuser',
            password='123',
            email='testuser@example.com'
        )
        data = self.data
        data['sender'] = self.testuser

        self.pmessages_model.objects.create(**self.data)

    def test_status_code(self):
        """Prueba varios caso de status_code."""
        self.logout()
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

        # Usuario login.
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'pmessages/inbox.html')

    def test_queryset(self):
        """Comprueba el get_queryset."""
        # Solo muestra cuando el recipient es el usuario.
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['inbox_list']), 3)
        self.logout()

        # perico
        perico = self.user_model.objects.get(pk=2)
        self.login(perico.username, '123')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['inbox_list']), 1)
        self.logout()

        # testuser
        self.login(self.testuser.username, '123')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['inbox_list']), 0)
        self.logout()

    def test_paginate_by(self):
        """Numero de paginación."""
        self.assertEqual(views.MessageInboxView.paginate_by, 10)


class MessageOutboxViewTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.data = self.load_data(
            os.path.join(os.path.dirname(__file__), 'pmessages_data.json')
        )
        # data requiere de instancias
        self.data['anuncio'] = self.anuncio_model.objects.get(pk=self.data['anuncio'])
        self.data['sender'] = self.user_model.objects.get(pk=self.data['sender'])
        self.data['recipient'] = self.user_model.objects.get(pk=self.data['recipient'])

        self.urlconf = 'pmessages:outbox'
        self.url = reverse(self.urlconf)
        self.login()

        # Crear un usuario nuevo y una alerta nueva.
        self.testuser = self.user_model.objects.create_user(
            username='testuser',
            password='123',
            email='testuser@example.com'
        )
        data = self.data
        data['sender'] = self.testuser

        self.pmessages_model.objects.create(**self.data)

    def test_status_code(self):
        """Prueba varios caso de status_code."""
        self.logout()
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

        # Usuario login.
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'pmessages/outbox.html')

    def test_queryset(self):
        """Comprueba el get_queryset."""
        # Solo muestra cuando el recipient es el usuario.
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['outbox_list']), 1)
        self.logout()

        # perico
        perico = self.user_model.objects.get(pk=2)
        self.login(perico.username, '123')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['outbox_list']), 2)
        self.logout()

        # testuser
        self.login(self.testuser.username, '123')
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['outbox_list']), 1)
        self.logout()

    def test_paginate_by(self):
        """Numero de paginación."""
        self.assertEqual(views.MessageInboxView.paginate_by, 10)


class ThreadListViewTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'pmessages:thread'
        self.url = reverse(self.urlconf, kwargs={'pk': 1})
        self.login()

    def test_status_code(self):
        """Prueba varios caso de status_code."""
        self.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        # Usuario login.
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.logout()

        # perico también puede ver el mismo outbox
        self.login(username='perico', password='123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'pmessages/thread.html')

    def test_queryset(self):
        """El queryset solo obtiene mensajes del sender y recipient."""
        user = self.user_model.objects.get(pk=1)
        thread_list = self.client.get(self.url).context['thread_list'][0]

        self.assertTrue(
            (user.username == thread_list.sender.username or
                user.username == thread_list.recipient.username)
        )


class MessageCreateViewTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.data = {
            "sender": 1,
            "recipient": 2,
            "body": "hola mundo",
            "subject": "Mensaje de prueba",
        }
        self.urlconf = 'pmessages:create'
        self.url = reverse(self.urlconf)
        self.login()

    def test_method_get_no_permitido(self):
        """Solo se permite post, pero probar get."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_post_crea_el_mensaje(self):
        """Prueba con form_valid, crea el mensaje, manda el Email y redirecciona
        a inbox.
        """
        old_messages_count = self.pmessages_model.objects.count()
        response = self.client.post(self.url, data=self.data, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('pmessages:inbox'),
            status_code=302,
            target_status_code=200
        )

        new_messages_count = self.pmessages_model.objects.count()

        self.assertGreater(new_messages_count, old_messages_count)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_invalid(self):
        """Redirecciona a inbox."""
        self.data['subject'] = 'abc'
        old_messages_count = self.pmessages_model.objects.count()
        response = self.client.post(self.url, data=self.data, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('pmessages:inbox'),
            status_code=302,
            target_status_code=200
        )

        new_messages_count = self.pmessages_model.objects.count()

        self.assertEqual(new_messages_count, old_messages_count)
        self.assertEqual(len(mail.outbox), 0)
