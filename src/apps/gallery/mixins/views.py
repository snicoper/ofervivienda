from django.shortcuts import Http404, get_object_or_404

from anuncios.models import Anuncio

from ..models import ImageAnuncio


class CheckIsOwnerByAnuncioIdMixin(object):
    """Comprueba que es el propietario por el id del anuncio."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anuncio = None

    def dispatch(self, request, *args, **kwargs):
        """Si el anuncio no pertenece al usuario, no podrá añadir la imagen al anuncio."""
        id_anuncio = kwargs.get('id_anuncio')
        self.anuncio = get_object_or_404(Anuncio, pk=id_anuncio)
        if self.anuncio.owner != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class CheckIsOwnerByImageIdMixin(object):
    """Comprueba que es el propietario por el id de la imagen.

    Attributes:
        anuncio (Anuncio): Anuncio al que pertenece la imagen.
    """
    anuncio = None

    def dispatch(self, request, *args, **kwargs):
        """Si la imagen no pertenece al usuario, no podrá cambiar la imagen del anuncio."""
        self.anuncio = get_object_or_404(ImageAnuncio, pk=kwargs.get('pk')).anuncio
        if self.anuncio.owner.id != request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
