from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as AuthUserChangeForm,
    UserCreationForm as AuthUserCreationForm,
)

from authentication.models import RegisterUser

from .models import User, UserLocation, UserOptions


class UserChangeForm(AuthUserChangeForm):
    """Form editar usuario en admin."""

    class Meta(AuthUserChangeForm.Meta):
        model = User


class UserProfileUpdateForm(forms.ModelForm):
    """Editar perfil de usuario por el propio usuario.

    La diferencia de UserChangeForm son los fields.
    """

    class Meta:
        _url_markdown = 'https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet'
        model = User
        fields = ('public_name', 'phone', 'description')
        help_texts = {
            'public_name': 'Nombre a mostrar en el perfil público y los anuncios.',
            'phone': (
                'Si se añade el teléfono y en opciones esta activo, se mostrara en el '
                'perfil público.'
            ),
            'description': (
                '<a href="{}" target="_blank">Markdown</a> permitido'.format(_url_markdown)
            )
        }


class UserCreationForm(AuthUserCreationForm):
    """Form crear usuario en admin."""

    email = forms.EmailField()

    class Meta(AuthUserCreationForm.Meta):
        model = User

    def clean_username(self):
        """Comprueba que username no este registrado.

        También lo prueba en la tabla RegisterUser.
        """
        username = self.cleaned_data["username"]
        if (User.objects.filter(username=username) or
                RegisterUser.objects.filter(username=username)):
            raise forms.ValidationError('El usuario ya existe en usuarios o registro temporal.')
        return username

    def clean_email(self):
        """Email no puede ser repetido.

        También lo prueba en la tabla RegisterUser
        """
        email = self.cleaned_data["email"]
        if (User.objects.filter(email=email) or
                RegisterUser.objects.filter(email=email)):
            raise forms.ValidationError('El Email ya existe en usuarios o registro temporal.')
        return email


class UserOptionsForm(forms.ModelForm):
    """Form para opciones de usuario."""

    class Meta:
        model = UserOptions
        fields = ('phone_public', 'address_public', 'email_public', 'notify_precio_anuncio_baja')
        help_texts = {
            'phone_public': (
                'Si esta activo y tienes numero de teléfono en el perfil, '
                'se añadirá por defecto a los anuncios y sera visible desde el '
                'perfil público.'
            ),
            'address_public': (
                'Sera mostrado en el perfil público. '
                '<strong>No recomendado para particulares</strong>'
            ),
            'email_public': 'Sera mostrado en el perfil público y en los anuncios.',
            'notify_precio_anuncio_baja': (
                'Recibirás notificaciones por email cuando los anuncios que tengas '
                'en favoritos bajen el precio.'
            )
        }


class UserUpdateAvatarForm(forms.ModelForm):
    """Form para añadir/cambiar el avatar del usuario."""
    delete_avatar = forms.BooleanField(
        label='Eliminar mi avatar',
        required=False
    )

    class Meta:
        model = User
        fields = ('avatar',)


class UserLocationUpdateForm(forms.ModelForm):
    """Actualizar localización del usuario."""

    class Meta:
        model = UserLocation
        fields = (
            'country',
            'state',
            'city',
            'address',
            'zipcode',
            'latitude',
            'longitude'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
