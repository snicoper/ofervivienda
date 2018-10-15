from django.urls import reverse


def get_client_ip(request):
    """Optener la IP del usuario."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_http_host(request):
    """Obtener url con http|https mas dominio.

    El dominio es el obtenido de request.get_host().

    Args:
        request (HttpRequest)

    Returns:
        str: Un string con el protocol y el domain http(s)://example.com/.
    """
    return '{}://{}'.format('https' if request.is_secure() else 'http', request.get_host())


def get_full_path(request, urlconf, **kwargs):
    """Compone un url completo con dominio y el urlconf.

    Args:
        request (HttpRequest)
        urlconf (str): Un URLConf valido.
        kwargs (dict): params del URLConf k=v, k2=v2.

    Returns:
        Un url completo http(s)://example.com/param1/param2/
    """
    domain = get_http_host(request)
    compose_url = '{}{}'.format(domain, reverse(urlconf, kwargs=kwargs))
    return compose_url
