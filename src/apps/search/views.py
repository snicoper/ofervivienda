from django.shortcuts import Http404
from django.views.generic import FormView, ListView

from anuncios.mixins.views import ClassFromCategoryNameMixin
from anuncios.models import Anuncio
from anuncios.settings import ANUNCIO_PAGINATE_BY
from favorites.mixins.views import FavoriteListContextMixin
from utils.text import ucfirst

from .forms import BaseSearchForm, SearchAddressForm


class IndexSearchView(FormView):
    """Form de búsqueda en el home.

    Cuando pulsa en buscar, lo procesa SearchFiltersView.
    """
    template_name = 'search/index.html'
    form_class = SearchAddressForm


class SearchFiltersView(FavoriteListContextMixin, ListView):
    """Form con filtros de busqueda."""
    template_name = 'search/search_filters.html'
    paginate_by = ANUNCIO_PAGINATE_BY
    context_object_name = 'anuncio_list'
    model = Anuncio

    def dispatch(self, request, *args, **kwargs):
        """Probar que la categoría del URLConf existe.

        Hay dos URLConf apuntan a la view, así que en caso de tener category,
        se ha de probar que existe.
        Si no hay category, muestra por defecto 'piso'.
        """
        self.category = 'piso'
        if self.kwargs.get('category'):
            self.category = self.kwargs.get('category')
            if not hasattr(self.model, self.category.upper()):
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        """Obtener el form en base a self.category."""
        form = BaseSearchForm.get_form_class(self.category)(self.request.GET or None)
        form.initial['category'] = self.category.upper()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['category_name'] = ucfirst(self.category)
        return context

    def get_queryset(self, **kwargs):
        """Queryset para búsquedas del formulario con filtros."""
        form = self.get_form()
        queryset = self.model.objects.none()
        if form.is_valid() and form.cleaned_data.get('q'):
            category = form.cleaned_data.get('category').upper()
            type_anuncio = form.cleaned_data.get('type_anuncio')
            metros_cuadrados = form.cleaned_data.get('metros_cuadrados', 0)
            habitaciones = form.cleaned_data.get('habitaciones', 0)
            banos = form.cleaned_data.get('banos', 0)
            precio = form.cleaned_data.get('precio', 0)
            genero = form.cleaned_data.get('genero', None)
            fumar_piso = form.cleaned_data.get('permite_fumar_piso', False)
            fumar_habitacion = form.cleaned_data.get('permite_fumar_habitacion', False)
            internet = form.cleaned_data.get('internet', False)
            address = form.cleaned_data.get('q')
            queryset = Anuncio.get_model_class(category).objects.published(
                location_string__search=address
            )
            if queryset.exists():
                # Filtros en la búsqueda.
                if type_anuncio:
                    queryset = queryset.filter(type_anuncio=type_anuncio)
                if habitaciones and habitaciones > 0:
                    queryset = queryset.filter(habitaciones__gte=habitaciones)
                if banos and banos > 0:
                    queryset = queryset.filter(banos__gte=banos)
                if metros_cuadrados and metros_cuadrados > 0:
                    queryset = queryset.filter(metros_cuadrados__gte=metros_cuadrados)
                if genero:
                    queryset = queryset.filter(genero=genero)
                if fumar_piso:
                    queryset = queryset.filter(permite_fumar_piso=fumar_piso)
                if fumar_habitacion:
                    queryset = queryset.filter(permite_fumar_habitacion=fumar_habitacion)
                if internet:
                    queryset = queryset.filter(internet=internet)
                if precio and precio > 0:
                    queryset = queryset.filter(precio__lte=precio)
        return queryset.select_related('owner').prefetch_related('image_anuncio')


class SearchMapView(ClassFromCategoryNameMixin, FormView):
    """Form avanzado de búsquedas, muestra mapa de gmaps."""
    template_name = 'search/search_map.html'
    form_class = None
    model = Anuncio

    def get(self, request, *args, **kwargs):
        """Comprueba que exista la categoría en el URLConf."""
        if not self.category or not hasattr(Anuncio, self.category):
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = {k: v for k, v in Anuncio.CATEGORY_CHOICES}
        context['title'] = category_list.get(self.category)
        context['category_name'] = self.category
        return context

    def get_form(self):
        """Obtener el form según category."""
        form_class = BaseSearchForm.get_form_class(self.category)
        initial = {'category': self.category}
        if self.request.user.is_authenticated and self.request.user.user_location:
            initial['latitude'] = self.request.user.user_location.latitude
            initial['longitude'] = self.request.user.user_location.longitude
        form = form_class(self.request.GET or None, initial=initial)
        # Eliminar el campo q
        del form.fields['q']
        return form
