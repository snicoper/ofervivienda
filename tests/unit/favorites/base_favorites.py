from favorites.models import Favorites
from tests.unit.base_test import BaseTestCase


class BaseFavoritesTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.favorites_model = Favorites
