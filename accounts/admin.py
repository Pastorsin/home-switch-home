from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Tarjeta, Banco, UsuarioEstandar


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (('User'), {
            'fields': ('first_name',
                       'last_name',
                       'email',
                       'is_staff',
                       'is_active',
                       )
        }),
    )
    list_display = ['email', 'first_name', 'last_name',
                    'is_staff', 'is_active', ]


admin.site.register(UsuarioEstandar)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tarjeta)
admin.site.register(Banco)
