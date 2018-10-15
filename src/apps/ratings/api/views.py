from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.views.generic import View

from anuncios.models import Anuncio

from ..models import Ratio


class AnuncioRatingApiView(LoginRequiredMixin, View):
    """Los usuarios autentificados votan un anuncio.

    Cuando se ha votado, devuelve el nuevo rating.
    """

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        score = request.GET.get('score')
        anuncio = get_object_or_404(Anuncio, pk=kwargs.get('anuncio_id'))
        ratio_obj = Ratio.objects.filter(user=request.user, anuncio=anuncio)
        if ratio_obj:
            ratio_obj.update(score=score)
        else:
            Ratio.objects.create(user=request.user, anuncio=anuncio, score=score)

        # Obtener el nuevo ratio.
        new_ratio = Ratio.objects.get_ratio_for_anuncio(anuncio)
        return HttpResponse(new_ratio)
