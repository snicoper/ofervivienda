from .base_pmessages import BasePmessagesTest


class MessageManagerTest(BasePmessagesTest):

    def setUp(self):
        super().setUp()

    def test_inbox_count_for(self):
        """Cuenta los mensajes que tiene en inbox."""
        # snicoper tiene 1
        snicoper = self.user_model.objects.get(pk=1)
        self.pmessages_model.objects.all().update(recipient_read=False)
        inbox_count = self.pmessages_model.objects.inbox_count_for(snicoper)

        self.assertEqual(inbox_count, 2)

        # Perico tiene 1
        perico = self.user_model.objects.get(pk=2)
        inbox_count = self.pmessages_model.objects.inbox_count_for(perico)

        self.assertEqual(inbox_count, 1)

        # snicoper tiene 0 y perico sigue teniendo 1
        snicoper = self.user_model.objects.get(pk=1)
        self.pmessages_model.objects.filter(recipient=snicoper).update(recipient_read=True)
        inbox_count = self.pmessages_model.objects.inbox_count_for(snicoper)

        self.assertEqual(inbox_count, 0)

        # Un usuario nuevo, tiene None
        new_user = self.user_model.objects.create_user(
            username='new_user',
            password='new_passowrd',
            email='new_user@example.com'
        )
        inbox_count = self.pmessages_model.objects.inbox_count_for(new_user)

        self.assertEqual(inbox_count, None)

    def test_get_thread(self):
        """En los fixtures hay 3 mensajes, 2 que perico ha mandado a snicoper
        ids 1 y 2, y un tercero que es una respuesta de snicoper a perico id 3,
        la respuesta (id 3), es al mensaje con id 1
        """
        message1 = self.pmessages_model.objects.get(pk=1)
        message2 = self.pmessages_model.objects.get(pk=2)
        thread_count1 = self.pmessages_model.objects.get_thread(message1.pk).count()
        thread_count2 = self.pmessages_model.objects.get_thread(message2.pk).count()

        self.assertEqual(thread_count1, 2)
        self.assertEqual(thread_count2, 1)
