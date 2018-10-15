from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import Http404, get_object_or_404
from django.views.generic import View

from anuncios.models import Anuncio


class FavoritesAddApiView(LoginRequiredMixin, View):
    """Añade un favorito."""

    def post(self, request, *args, **kwargs):
        """En AJAX se ha de pasar el ID del anuncio."""
        if not request.is_ajax():
            raise Http404
        anuncio_id = request.POST.get('anuncio_id')
        anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
        try:
            favorites = request.user.favorites_user
            if anuncio not in favorites.anuncios.all():
                favorites.anuncios.add(anuncio)
        except:
            pass
        return JsonResponse({'add': True})


class FavoritesRemoveApiView(LoginRequiredMixin, View):
    """Elimina un favorito."""

    def post(self, request, *args, **kwargs):
        """En AJAX se ha de pasar el ID del anuncio."""
        if not request.is_ajax():
            raise Http404
        anuncio_id = request.POST.get('anuncio_id')
        anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
        try:
            favorites = request.user.favorites_user
            if anuncio in favorites.anuncios.all():
                favorites.anuncios.remove(anuncio)
        except:
            pass
        return JsonResponse({'remove': True})
