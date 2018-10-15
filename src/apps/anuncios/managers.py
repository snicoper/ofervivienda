from model_utils.managers import InheritanceManager


class AnuncioManager(InheritanceManager):

    def published(self, **kwargs):
        """Solo los anuncios activos."""
        return self.get_queryset().filter(active=True, **kwargs)
