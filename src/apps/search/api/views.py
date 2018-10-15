from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from anuncios.api.serializers import BaseAnuncioSerializer
from anuncios.models import Anuncio


class SearchMarkersPositionsAPIView(ListAPIView):
    """Búsqueda con geolocation."""
    queryset = Anuncio.objects.published()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        category = self.request.GET.get('category')
        return BaseAnuncioSerializer.get_serializer_class(category)

    def get_queryset(self):
        # Se obtienen en metros y se pasan a kilómetros.
        radius = float(self.request.GET.get('radius')) / 1000.0
        category = self.request.GET.get('category').upper()
        latitude = float(self.request.GET.get('latitude'))
        longitude = float(self.request.GET.get('longitude'))
        point = Point(longitude, latitude)
        type_anuncio = self.request.GET.get('type_anuncio')
        genero = self.request.GET.get('genero')
        # Campos integer.
        metros_cuadrados = self._to_int(self.request.GET.get('metros_cuadrados'))
        habitaciones = self._to_int(self.request.GET.get('habitaciones'))
        banos = self._to_int(self.request.GET.get('banos'))
        precio = self._to_int(self.request.GET.get('precio'))
        # Campos boolean.
        fumar_piso = self._boolean_value(self.request.GET.get('permite_fumar_piso'))
        fumar_habitacion = self._boolean_value(self.request.GET.get('permite_fumar_habitacion'))
        internet = self._boolean_value(self.request.GET.get('internet', 'false'))
        # queryset
        queryset = Anuncio.get_model_class(category).objects.published(
            point__distance_lte=(point, Distance(km=radius))
        )
        # filtros.
        if queryset.exists():
            if type_anuncio:
                queryset = queryset.filter(type_anuncio=type_anuncio)
            if habitaciones and habitaciones > 0:
                queryset = queryset.filter(habitaciones__gte=habitaciones)
            if banos and banos > 0:
                queryset = queryset.filter(banos__gte=banos)
            if metros_cuadrados and metros_cuadrados > 0:
                queryset = queryset.filter(metros_cuadrados__gte=metros_cuadrados)
            if precio and precio > 0:
                queryset = queryset.filter(precio__lte=precio)
            if genero:
                queryset = queryset.filter(genero=genero)
            if fumar_piso:
                queryset = queryset.filter(permite_fumar_piso=fumar_piso)
            if fumar_habitacion:
                queryset = queryset.filter(permite_fumar_habitacion=fumar_habitacion)
            if internet:
                queryset = queryset.filter(internet=internet)
        return queryset

    def _to_int(self, value):
        """Valor to integer, comprueba si tiene valor.

        Returns:
            int: El valor como int si tiene un valor, 0 en caso contrario.
        """
        if value:
            return int(value)
        return 0

    def _boolean_value(self, value):
        """El campo del form se obtiene 'on' o '', lo convierte en booleano.

        Args:
            value (str): El valor del campo.

        Returns:
            bool: True si el valor es 'on', False en caso contrario.
        """
        return True if value == 'on' else False
