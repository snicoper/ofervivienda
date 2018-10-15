from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User, UserLocation, UserOptions


class UserOptionsInline(admin.StackedInline):
    """Opciones inline del usuario en UserAdmin."""
    model = UserOptions


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [UserOptionsInline]
    list_display = (
        'username',
        'email',
        'is_premium',
        'expire_premium_at',
        'anuncios_premium',
        'is_staff'
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'avatar',
                'public_name',
                'first_name',
                'last_name',
                'email',
                'phone',
                'slug'
            )
        }),
        (_('Descripción'), {
            'fields': ('description',)
        }),
        (_('Premium Account'), {
            'fields': ('is_premium', 'expire_premium_at', 'anuncios_premium')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    """UserLocation en admin."""
    list_display = ('__str__', 'location_string')
