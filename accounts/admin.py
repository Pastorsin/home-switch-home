from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (('User'), {
            'fields': ('username', 'password', 'email',
                       'is_staff', 'edad', 'es_premium')
        }),
    )
    list_display = ['email', 'username', 'edad', 'is_staff', 'es_premium', ]


admin.site.register(CustomUser, CustomUserAdmin)
