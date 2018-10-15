from django import template
from django.utils import timezone

from ..settings import ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT

register = template.Library()


@register.simple_tag
def can_upload_update_at(anuncio):
    """Prueba si el anuncio es premium o si ya han pasado los días de
    ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT.

    Args:
        anuncio (Anuncio): Object Anuncio.

    Returns:
        str: "True" si puede actualizarlo, "False" si no es premium.
        Si el anuncio es premium pero aun no puede actualizarlo, devolverá
        los días que falta para actualizarlo "26 de Marzo de 2017 a las 21:16".
        IMPORTANTE: "True" y "False" son strings.
    """
    if not anuncio.is_premium:
        return "False"
    now = timezone.now()
    rest_now = now - timezone.timedelta(days=ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT)
    if anuncio.update_at <= rest_now:
        return "True"
    return anuncio.update_at + timezone.timedelta(days=ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT)
