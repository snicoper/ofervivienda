from django import template

register = template.Library()


@register.filter(name='get_card_info')
def get_card_info(card_info, forloop):
    """Obtener datos de información de una card.

    Se utiliza en src/templates/payments/process_x_premium.html, para obtener el key de card_info.

    Args:
        card_info (list): Lista con la información de la card.
        forloop (int): El string numérico del valor de for.forloop0.

    Example:
        {% with card_info|get_card_info:forloop.counter0 as card_info %}
          hacer algo con card_info...
        {% endwith %}

    Returns:
        card_info[x] (dict): Diccionario con los datos de información de la card.
    """
    return card_info[int(forloop)]
