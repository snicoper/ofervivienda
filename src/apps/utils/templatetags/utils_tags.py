import locale

from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()


@register.simple_tag(name='markdown')
def markdown_format(text, safe=False):
    """Devuelve el texto markdown en HTML.

    Example:
        Con un texto seguro.
        {% markdown obj.description safe=True %}
        {% markdown obj.description True %}

        Con un texto inseguro.
        {% markdown obj.description safe=False %}
        {% markdown obj.description False %}
        {% markdown obj.description %}

    Args:
        text (str): Texto markdown
        safe (bool): El texto es seguro? de lo contrario lo escapa.

    Returns:
        str: El markdown convertido en HTML.
    """
    if not safe:
        # Si no es safe, el texto siempre se escapa.
        text = escape(text)
    return mark_safe(
        markdown2.markdown(
            text,
            extras=['fenced-code-blocks']
        )
    )


@register.simple_tag(takes_context=True)
def is_active(context, urlconf_name, **kwargs):
    """Devolverá active si request.path coincide con urlconf_name.

    Comprueba con URLConf con request.path.

    Example:
        <li class="{% is_active 'blog:article_list' %}">

    Args:
        context: Contexto en el template.
        urlconf_name (str): URLConf
        kwargs (dict): parámetros de reverse('', kwargs=kwargs)

    Returns:
        (str): si coincide devolverá 'active' en caso contrario un string vació ''.
    """
    url_reverse = reverse(urlconf_name, kwargs=kwargs)
    if context['request'].path == url_reverse:
        return ' active'
    return ''


@register.simple_tag(name='next_pagination', takes_context=True)
def next_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina siguiente si existe.

    Example:
        <a href="{% next_pagination %}">next</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte del
    '?page=xxx' por el nuevo numero de pagina. En caso contrario, añadirá
    'page=xxx' al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.next_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.next_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.next_page_number())


@register.simple_tag(name='previous_pagination', takes_context=True)
def previous_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina previa si existe.

    Example:
        <a href="{% previous_pagination %}">previous</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte
    del ?page=xxx por el nuevo numero de pagina. En caso contrario,
    añadirá page=xxx al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.previous_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.previous_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.previous_page_number())


@register.simple_tag(name='display_for')
def display_for(value, typeof='bool', klass=''):
    """Dependiendo del valor, muestra en html una representación del valor.

    Por defecto trata el valor como un boolean.

    Example:
        {% display_for options.is_public %}
        {% display_for options.is_public 'bool' %}
        {% display_for options.is_public 'bool' 'text-warning' %}

    Args:
        value (mixed): Valor a obtener una representación HTML.
        typeof (str): Tipo esperado, bool, number, str.
        klass (str): Clases css.

    Returns:
        str: HTML como representación del valor, mismo valor si aun no tiene
             una representación implementada.
    """
    # Booleans.
    if typeof == 'bool':
        if value is True:
            value = '<i class="material-icons text-success md-3 {}">check_circle</i>'.format(klass)
        else:
            value = '<i class="material-icons text-danger md-3 {}">cancel</i>'.format(klass)
    # Numbers.
    if typeof in 'number':
        if int(value) > 0:
            value = '<span class="badge badge-success {}">{}</span>'.format(klass, value)
        else:
            value = '<span class="badge badge-secondary {}">{}</span>'.format(klass, value)
    # Strings.
    if typeof == 'str':
        value = '<span class="badge badge-primary {}">{}</span>'.format(klass, value)
    return mark_safe(value)


# FILTERS

@register.filter('currency')
def currency(anuncio):
    """Obtener la representacion del symbol según la moneda.

    Formatea el precio según el simbolo.

    En sur america, usa el dollar.

    Args:
        anuncio (AbstractAnuncioModel)

    Returns:
        EUR = 100 €
        USD = $ 100
        GBP = £ 100
        En caso de no tener currency, devolverá una cadena vaciá.
    """
    current_locale = locale.getlocale()
    locales = {
        'EUR': 'es_ES',
        'USD': 'en_US',
        'GBP': 'en_GB'
    }
    locale.setlocale(locale.LC_ALL, locales.get(anuncio.currency, 'es_ES'))
    locale_format = locale.format('%d', anuncio.precio, grouping=True)
    symbol = anuncio.get_currency_display()
    currency_swith = {
        'EUR': '{} {}'.format(locale_format, symbol),
        'USD': '{} {}'.format(symbol, locale_format),
        'GBP': '{} {}'.format(symbol, locale_format),
    }
    locale.setlocale(locale.LC_ALL, current_locale)
    return currency_swith.get(anuncio.currency, '')
