from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Promo

UserModel = get_user_model()


class GenerateCodePromoToUserForm(forms.ModelForm):
    """Form para generar un código de promoción y notificarlo a un usuario especifico."""
    to_user = forms.IntegerField(
        label='ID Usuario'
    )

    class Meta:
        model = Promo
        fields = ('payment_promo',)

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']
        try:
            UserModel.objects.get(pk=to_user)
        except UserModel.DoesNotExist:
            msg_error = 'La ID del usuario no existe'
            raise forms.ValidationError(msg_error)
        return to_user


class PromoValidateCodeForm(forms.Form):
    """Formulario para validar un código promo por parte de un usuario."""
    code = forms.CharField(
        max_length=12,
        label='Inserta el código de promoción'
    )

    def clean_code(self):
        """Comprueba que el código sea valido."""
        code = self.cleaned_data['code']
        promo = Promo.objects.filter(code=code)
        if not promo:
            msg_error = 'El código insertado no es valido'
            raise forms.ValidationError(msg_error)

        # Comprueba que no haya expirado.
        if promo[0].expire_at < timezone.now():
            msg_error = 'El código insertado parece que ha caducado'
            raise forms.ValidationError(msg_error)

        # Comprueba que no haya sido utilizado.
        if promo[0].active:
            msg_error = 'El código insertado ya se ha usado'
            raise forms.ValidationError(msg_error)
        return code
