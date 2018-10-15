class FavoriteListContextMixin(object):
    """Añade al contexto una variable con la lista (PKs) de favoritos.

    Motivos:
        Al hacer una consulta por cada "anuncio in lista_favoritos" en templatetags
        o desde /src/apps/favorites/templates/favorites/_heart_favorites.html
        puede crear una consulta para cada anuncio.
        De esta manera se añade en una consulta en el contexto con todas los
        favoritos del usuario.
    """

    def get_context_data(self, **kwargs):
        """Añadir en el contexto favorite_list_by_owner, que son favoritos del
        usuario.

        Utilizado en src/apps/favorites/templates/favorites/_heart_favorites.html

        Example:
            Desde el template.
            {% if anuncio.pk in favorite_list_by_owner %}{% endif %}

        Returns:
            list: Una lista con los PKs de los anuncios en favoritos, si no
            tiene favoritos, la lista estará vacía.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            queryset = self.request.user.favorites_user.anuncios.all().values('pk')
            values_to_list = [item['pk'] for item in queryset]
            context['favorite_list_by_owner'] = values_to_list
        return context
