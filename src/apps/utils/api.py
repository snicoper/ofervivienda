from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.generic import View

from .gmaps import user_ip_info
from .http import get_client_ip


class UserIpInfoApiView(View):
    """Obtener información de localización del usuario.

    NOTA: En local no funciona, por lo que si se esta en DEBUG=True, se le
    pondrá una IP.

    Hay un maximo de 15.000 peticiones por hora, por eso esta puesto como API.

    Returns:
        json: Datos en json, listo para usar desde javascript.
    """

    def get(self, request, *args, **kwargs):
        if not settings.DEBUG:
            client_ip = get_client_ip(request)
        else:
            client_ip = '90.77.76.108'
        return HttpResponse(user_ip_info(client_ip) or {'BAD'})
