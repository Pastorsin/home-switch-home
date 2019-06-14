# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from datetime import date
from .models import CustomUser


class CustomUserForm:

    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        today = date.today()
        diferencia_de_años = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if diferencia_de_años < 18:
            raise ValidationError('Lo sentimos, para utilizar esta pagina debe ser mayor de edad')
        return data

class CustomUserCreationForm(UserCreationForm, CustomUserForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'foto', 'fecha_nacimiento', 'dni')


class CustomUserChangeForm(UserChangeForm, CustomUserForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'foto', 'fecha_nacimiento', 'dni')
