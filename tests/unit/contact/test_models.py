import os

from tests.unit.images import simple_uploaded_file

from .base_contact import BaseContactTest


class ContactMessageTest(BaseContactTest):

    def setUp(self):
        super().setUp()
        self.data = {
            'subject': 'Mensaje test',
            'message': 'Mensaje de prueba',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'is_register': False
        }
        self.message = self.contact_model.objects.create(**self.data)

    def test_nuevo_mensaje(self):
        """Comprueba un nuevo mensaje."""
        self.assertEqual(self.contact_model.objects.count(), 1)

    def test_str(self):
        """Prueba __str__."""
        self.assertEqual(str(self.message), self.data['subject'])

    def test_read_default_false(self):
        """Por defecto read es False."""
        self.assertFalse(self.message.read)

    def test_eliminar_message_elimina_imagen(self):
        """Al eliminar un mensaje, eliminara la imagen."""
        image_path = os.path.join(os.path.dirname(__file__), 'avatar.jpg')
        self.data['screenshot'] = simple_uploaded_file(image_path)
        message = self.contact_model.objects.create(**self.data)
        message_image_path = message.screenshot.path

        self.assertTrue(message_image_path)
        self.assertTrue(os.path.exists(message_image_path))

        # Eliminar el mensaje eliminara la imagen.
        message.delete()

        self.assertFalse(os.path.exists(message_image_path))
