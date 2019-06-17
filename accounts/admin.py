from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Tarjeta, Banco


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (('User'), {
            'fields': ('first_name',
                       'last_name',
                       'password',
                       'email',
                       'is_staff',
                       'fecha_nacimiento',
                       'es_premium',
                       'dni',
                       'tarjeta',
                       'creditos')
        }),
    )
    list_display = ['email', 'first_name', 'last_name',
                    'fecha_nacimiento', 'is_staff', 'es_premium', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tarjeta)
admin.site.register(Banco)
