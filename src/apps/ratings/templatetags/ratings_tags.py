from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_score_for_anuncio(context, anuncio):
    """Obtener el score de un usuario en un anuncio.

    Args:
        context (Context): HttpContext
        anuncio (Anuncio): El anuncio a comprobar.

    Returns:
        int: El score del usuario sobre el anuncio, 0 en caso
        de que el usuario no haya votado sobre el anuncio.
    """
    request = context['request']
    if not request.user.is_authenticated:
        return 0
    score = anuncio.ratio_anuncio.filter(user=request.user)
    if not score:
        return 0
    return score[0].score
