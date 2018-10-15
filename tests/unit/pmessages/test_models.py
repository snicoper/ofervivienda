import os

from .base_pmessages import BasePmessagesTest


class MessageTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()
        self.data = self.load_data(os.path.join(os.path.dirname(__file__), 'pmessages_data.json'))
        self.anuncio = self.anuncio_model.objects.get(pk=self.data['anuncio'])
        self.data['anuncio'] = self.anuncio
        self.data['sender'] = self.user_model.objects.get(pk=self.data['sender'])
        self.data['recipient'] = self.user_model.objects.get(pk=self.data['recipient'])

    def test_create_object(self):
        """Crea un objeto."""
        self.pmessages_model.objects.create(**self.data)

        # 2 enviados por perico y una respuesta de snicoper,
        # mas el recién creado = 4.
        self.assertEqual(self.pmessages_model.objects.count(), 4)

    def test_create_sin_anuncio(self):
        """Anuncio en null=True."""
        self.data['anuncio'] = None
        message = self.pmessages_model.objects.create(**self.data)

        self.assertTrue(message)

    def test_parent(self):
        """Parent ha de ser instancia de otro Message."""
        message = self.pmessages_model.objects.get(pk=1)
        self.data['parent'] = message
        message = self.pmessages_model.objects.create(**self.data)

        self.assertTrue(message)

    def test_read_por_defecto_false(self):
        """Por defecto recipient_read es False."""
        message = self.pmessages_model.objects.create(**self.data)

        self.assertFalse(message.recipient_read)

    def test_ordering_default(self):
        """Comprobar el Meta.ordering."""
        expected_ordering = ('recipient_read', '-sent_at',)
        ordering_model = self.pmessages_model._meta.ordering

        self.assertEqual(ordering_model, expected_ordering)

    def test_str(self):
        """Se espera el titulo del mensaje."""
        message = self.pmessages_model.objects.create(**self.data)

        self.assertEqual(str(message), self.data['subject'])
