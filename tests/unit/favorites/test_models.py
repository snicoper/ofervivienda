from .base_favorites import BaseFavoritesTest


class Favorites(BaseFavoritesTest):

    def setUp(self):
        super().setUp()

    def test_anadir_favorites(self):
        """Prueba añadir favoritos.

        Cuando se crea un usuario, se le crea un Favorites object, por eso que
        hay 2 registros.
        """
        self.assertEqual(self.favorites_model.objects.count(), 2)
        user = self.user_model.objects.get(pk=1)

        self.assertEqual(user.favorites_user.anuncios.count(), 0)
        anuncios = self.anuncio_model.objects.all()[:5]
        for anuncio in anuncios:
            user.favorites_user.anuncios.add(anuncio)

        favorites_user = self.favorites_model.objects.get(owner=user)

        self.assertEqual(favorites_user.anuncios.count(), 5)
