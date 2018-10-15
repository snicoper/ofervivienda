from django.db.models import Manager, Q


class MessageManager(Manager):

    def inbox_count_for(self, user):
        """Obtener total de mensajes sin leer.

        Returns:
            int|bool: Si no ha enviado ni recibido devolverá None, si ha enviado
            y/o recibido pero no tiene mensajes sin leer 0 y si ha enviado y/o
            recibido y ademas tiene mensajes sin leer, devolverá la cantidad de
            mensajes que tiene sin leer.
        """
        queryset = self.filter(Q(sender=user) | Q(recipient=user))
        if not queryset.exists():
            return None
        queryset = self.filter(recipient=user, recipient_read=False)
        if not queryset.exists():
            return 0
        return queryset.count()

    def get_thread(self, message_id):
        """Obtiene todo el thread de un message concreto."""
        return self.filter(
            Q(message_parent__pk=message_id) | Q(parent=message_id) | Q(pk=message_id)
        )
