import sys

from rest_framework.serializers import ModelSerializer

from gallery.api.serializers import ImageAnuncioSerializer
from utils.text import ucfirst

from ..models import (
    Anuncio, AnuncioApartamento, AnuncioCasa, AnuncioHabitacion,
    AnuncioIndustrial, AnuncioLocal, AnuncioParking, AnuncioPiso,
    AnuncioTerreno,
)


class AnuncioUpdateAtSerializer(ModelSerializer):
    """Serializer para actualizar el campo update_at."""

    class Meta:
        model = Anuncio
        fields = ('update_at',)


class AnunciosSerializer(ModelSerializer):
    """Serializer global de Anuncios."""
    image_anuncio = ImageAnuncioSerializer(many=True, read_only=True)

    class Meta:
        model = Anuncio
        fields = (
            'pk',
            'location_string',
            'metros_cuadrados',
            'latitude',
            'longitude',
            'precio',
            'currency',
            'image_anuncio',
        )


class BaseAnuncioSerializer(AnunciosSerializer):
    """Base serializer, para obtener un serializer de una clase concreta."""

    @staticmethod
    def get_serializer_class(model_name):
        """Obtener un serializer según model_name."""
        module = sys.modules[__name__]
        object_model = 'Anuncio{}Serializer'.format(ucfirst(model_name))
        if hasattr(module, object_model):
            return getattr(module, object_model)
        msg_error = 'El serializer {} no ha sido creado'.format(object_model)
        raise NotImplementedError(msg_error)


class BaseAnuncioViviendaSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer.Meta):
        fields = BaseAnuncioSerializer.Meta.fields + (
            'habitaciones',
            'banos',
            'ano_construccion',
            'parking',
        )


class AnuncioPisoSerializer(BaseAnuncioViviendaSerializer):

    class Meta(BaseAnuncioViviendaSerializer):
        model = AnuncioPiso
        fields = BaseAnuncioViviendaSerializer.Meta.fields


class AnuncioCasaSerializer(BaseAnuncioViviendaSerializer):

    class Meta(BaseAnuncioViviendaSerializer):
        model = AnuncioCasa
        fields = BaseAnuncioViviendaSerializer.Meta.fields


class AnuncioApartamentoSerializer(BaseAnuncioViviendaSerializer):

    class Meta(BaseAnuncioViviendaSerializer):
        model = AnuncioApartamento
        fields = BaseAnuncioViviendaSerializer.Meta.fields


class AnuncioHabitacionSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer):
        model = AnuncioHabitacion
        fields = BaseAnuncioSerializer.Meta.fields + (
            'permite_fumar_piso',
            'permite_fumar_habitacion',
            'internet',
        )


class AnuncioTerrenoSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer):
        model = AnuncioTerreno
        fields = BaseAnuncioSerializer.Meta.fields


class AnuncioParkingSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer):
        model = AnuncioParking
        fields = BaseAnuncioSerializer.Meta.fields


class AnuncioIndustrialSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer):
        model = AnuncioIndustrial
        fields = BaseAnuncioSerializer.Meta.fields


class AnuncioLocalSerializer(BaseAnuncioSerializer):

    class Meta(BaseAnuncioSerializer):
        model = AnuncioLocal
        fields = BaseAnuncioSerializer.Meta.fields
