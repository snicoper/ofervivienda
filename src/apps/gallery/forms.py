from django import forms

from .models import ImageAnuncio


class ImageAnuncioForm(forms.ModelForm):
    """Form para una imagen de un anuncio."""

    class Meta:
        model = ImageAnuncio
        fields = ('image', 'anuncio', 'description')
        widgets = {
            'anuncio': forms.HiddenInput()
        }


class ImageAnuncioCreateForm(ImageAnuncioForm):
    """Cuando se crean las imágenes, no requiere ningún campo.

    Luego en la view, si un campo no tiene image, simplemente no la añade y
    no crea el objeto (usa formsets).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['anuncio'].required = False
