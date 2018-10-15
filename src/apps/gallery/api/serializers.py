from rest_framework import serializers

from ..models import ImageAnuncio


class ImageAnuncioSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageAnuncio
        fields = ('image', 'thumbnail', 'description')
