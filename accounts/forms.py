# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from datetime import date
from .models import CustomUser, Tarjeta


class CustomUserForm:

    URL_FOTO_ANONIMA = 'http://sport-werkt.nl/wp-content/uploads/2018/12/profile.png'

    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        today = date.today()
        diferencia_de_años = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if diferencia_de_años < 18:
            raise ValidationError(
                'Tenes que ser mayor de 18 años para acceder al sistema')
        return data

    def clean_dni(self):
        data = self.cleaned_data['dni']
        if not (len(data) == 8 and data.isdigit()):
            raise ValidationError(
                'El DNI debe tener 8 digitos sin separadores. Ej: 11222333')
        return data

    def clean_foto(self):
        data = self.cleaned_data['foto']
        if not data:
            data = self.URL_FOTO_ANONIMA
        return data


class CustomUserCreationForm(UserCreationForm, CustomUserForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'foto', 'fecha_nacimiento', 'dni')


class CustomUserChangeForm(UserChangeForm, CustomUserForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'foto', 'fecha_nacimiento', 'dni')


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('numero', 'nombre_completo', 'fecha_vencimiento', 'cvc', 'banco')

    MSG_FECHA_INVALIDA = 'Ingrese una fecha de vencimiento válida porfavor'

    def clean_fecha_vencimiento(self):
        data = self.cleaned_data['fecha_vencimiento']
        fecha = data.split('/')
        mes = fecha[0]
        try:
            año = fecha[1]
        except IndexError:
            raise ValidationError(self.MSG_FECHA_INVALIDA)
        else:
            if len(año.strip()) < 4 or int(mes) > 12:
                raise ValidationError(self.MSG_FECHA_INVALIDA)
        return data
