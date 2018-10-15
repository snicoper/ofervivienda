from django.shortcuts import get_object_or_404


class ClassFromIDMixin(object):
    """Mixin para obtener la clase del modelo dinámicamente.

    Obtiene una subclase de la clase Anuncio por el ID de la URLConf.

    Requiere que la clase que utiliza el mixin añada la propiedad model = Anuncio.

    Después estará disponible en toda la clase la propiedad self.category, con el
    nombre de category en uppercase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def get_queryset(self):
        # Requiere una consulta extra para obtener la categoría del anuncio.
        self.category = get_object_or_404(self.model, pk=self.kwargs.get('pk')).category
        self.model = self.model.get_model_class(self.category)
        return super().get_queryset()


class ClassFromCategoryNameMixin(object):
    """Mixin para obtener la clase del modelo dinamicamente.

    Obtiene una subclase de la clase Anuncio por el category de la URLConf.

    Requiere que la clase que utiliza el mixin añada la propiedad model = Anuncio.

    Después estará disponible en toda la clase la propiedad self.category, con el
    nombre de category en uppercase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = self.kwargs.get('category').upper()
        self.model = self.model.get_model_class(self.category)
        return super().dispatch(request, *args, **kwargs)
