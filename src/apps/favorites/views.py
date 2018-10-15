from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DeleteView, ListView

from anuncios.settings import ANUNCIO_PAGINATE_BY

from .mixins.views import FavoriteListContextMixin
from .models import Favorites


class FavoritesListView(LoginRequiredMixin, FavoriteListContextMixin, ListView):
    """Anuncios favoritos de un usuario."""
    template_name = 'favorites/favorites_list.html'
    context_object_name = 'anuncio_list'
    paginate_by = ANUNCIO_PAGINATE_BY
    model = Favorites

    def get_queryset(self):
        """Se obtiene el ID del usuario actual."""
        queryset = Favorites.objects.get(owner=self.request.user)
        return queryset.anuncios.published(). select_related('owner').\
            prefetch_related('image_anuncio').select_subclasses()


class FavoriteUserListDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar lista de favoritos de un usuario."""
    template_name = 'favorites/delete_all.html'
    context_object_name = 'favorite_list'
    model = Favorites

    def get_object(self):
        """Obtener favoritos según Usuario."""
        return get_object_or_404(Favorites, owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Si viene del form, eliminar los resources de favorite."""
        favorites = self.get_object()
        favorites_list = favorites.anuncios.all()
        if favorites_list:
            for favorite in favorites_list:
                favorites.anuncios.remove(favorite)
            msg_success = 'Se han eliminado todos los anuncios de favoritos.'
            messages.success(request, msg_success)
        else:
            msg_info = 'No hay favoritos para eliminar'
            messages.info(request, msg_info)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('favorites:list')
