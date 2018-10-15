from django import template

register = template.Library()


@register.filter(name='to_list')
def to_list(anuncio):
    """Convierte un anuncio en una lista de anuncios.

    Para aprovechar src/templates/anuncios/_anuncio_list.html que requiere de
    una lista de anuncios.

    Example:
        {{ anuncio|to_list }}

    Args:
        anuncio (Anuncio): Anuncio.

    Returns:
        list[Anuncios]: Lista de anuncios.
    """
    return [anuncio]
