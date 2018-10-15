from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

from utils.http import get_full_path
from utils.mail import send_templated_mail

from .models import AlertAnuncio


def alerts_users_new_anuncio(anuncio, request):
    """Enviá un email si coincide con los alerts.

    Hace las consultas por NORMAL, RADIUS y POLYGON, después elimina duplicados
    y los manda por email las alertas.

    Args:
        anuncio (Anuncio): Anuncio recién creado.
        request (HttpRequest): Objeto request.

    Returns:
        int: 1 si todo va bien, 0 en caso contrario.
    """
    model = AlertAnuncio.get_model_class(anuncio.category)
    queryset = model.objects.filter(polygon__contains=anuncio.point)
    if queryset.exists():
        queryset = _default_queryset(anuncio, queryset).exclude(owner=anuncio.owner)
    if queryset.exists():
        return _send_mails(anuncio, queryset, request)
    return 1


def _default_queryset(anuncio, queryset):
    """Filtra campos por defecto valido para todos los type_alert.

    Args:
        anuncio (Anuncio): Anuncio recién creado.
        queryset (AlertAnuncio): Un queryset ya comenzado.

    Returns:
        AlertAnuncio: El queryset con los filtros.
    """
    queryset = queryset.filter(type_anuncio=anuncio.type_anuncio)
    queryset = queryset.filter(Q(precio=0) | Q(precio__gte=anuncio.precio))
    if hasattr(anuncio, 'metros_cuadrados') and anuncio.metros_cuadrados:
        queryset = queryset.filter(
            Q(metros_cuadrados=0) |
            Q(metros_cuadrados__lte=anuncio.metros_cuadrados)
        )
    if hasattr(anuncio, 'estado_inmueble') and anuncio.estado_inmueble:
        queryset = queryset.filter(
            Q(estado_inmueble__isnull=True) |
            Q(estado_inmueble=anuncio.estado_inmueble)
        )
    if hasattr(anuncio, 'habitaciones') and anuncio.habitaciones:
        queryset = queryset.filter(
            Q(habitaciones=0) |
            Q(habitaciones__lte=anuncio.habitaciones)
        )
    if hasattr(anuncio, 'banos') and anuncio.banos:
        queryset = queryset.filter(
            Q(banos=0) |
            Q(banos__lte=anuncio.banos)
        )
    if anuncio.category == anuncio.HABITACION:
        queryset = queryset.filter(
            Q(permite_fumar_piso=False) |
            Q(permite_fumar_piso=anuncio.permite_fumar_piso)
        )
        queryset = queryset.filter(
            Q(permite_fumar_habitacion=False) |
            Q(permite_fumar_habitacion=anuncio.permite_fumar_habitacion)
        )
        queryset = queryset.filter(
            Q(internet=False) |
            Q(internet=anuncio.internet)
        )
        if anuncio.genero:
            queryset = queryset.filter(genero=anuncio.genero)
    return queryset


def _send_mails(anuncio, alerts, request):
    """Enviá un email a los usuarios.

    Enviá el email a todos los usuarios que tienen un filtro coincidente al
    anuncio recién creado.

    Args:
        alerts (QuerySet): Resultados de la búsqueda.
        request (HttpRequest): Objeto request.

    Returns:
        int: 1 si se manda el email, 0 en caso contrario.
    """
    current_site = get_current_site(request)
    recipients = set([alert.owner.email for alert in alerts])
    anuncio_url = get_full_path(request, 'anuncios:details', pk=anuncio.pk)
    alerts_url = get_full_path(request, 'accounts:profile')
    return send_templated_mail(
        subject='Anuncio que puede interesarte desde {}'.format(current_site.name),
        from_email=settings.GROUP_EMAILS['NO-REPLY'],
        recipients=list(recipients),
        context={
            'site_name': current_site.name,
            'anuncio': anuncio,
            'anuncio_url': anuncio_url,
            'alerts_url': alerts_url
        },
        template_text='alerts/emails/alert_anuncio.txt'
    )
