from django.utils import timezone

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Anuncio
from ..settings import ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT
from .serializers import AnuncioUpdateAtSerializer


class AnuncioUpdateAtUpdateAPIView(UpdateAPIView):
    """Actualiza el campo update_at del anuncio.

    Requiere Login del usuario, que el usuario sea el owner del anuncio y que
    el anuncio sea premium.
    Ademas, requiere que el anuncio se haya actualizado un mínimo de
    ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT.

    Si todo OK, retorna has_update true, en caso contrario has_update false.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AnuncioUpdateAtSerializer

    def update(self, request, *args, **kwargs):
        time_diff = timezone.now() - timezone.timedelta(days=ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT)
        try:
            anuncio = Anuncio.objects.get(pk=kwargs.get('pk'), update_at__lte=time_diff)
        except Anuncio.DoesNotExist:
            return Response({'has_update': False})
        if anuncio.owner != request.user or not anuncio.is_premium:
            return Response({'has_update': False})
        anuncio.update_at = timezone.now()
        anuncio.save()
        return Response({'has_update': True})
