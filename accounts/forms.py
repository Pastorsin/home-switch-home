# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from datetime import date
from .models import CustomUser, Tarjeta


class CustomUserForm:

    URL_FOTO_ANONIMA = 'http://sport-werkt.nl/wp-content/uploads/2018/12/profile.png'
    MSG_EDAD_INVALIDA = 'Tenes que ser mayor de 18 años para acceder al sistema'
    MSG_DNI_INVALIDO = 'El DNI debe tener 8 digitos sin separadores. Ej: 11222333'

    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        today = date.today()
        diferencia_de_años = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if diferencia_de_años < 18:
            raise ValidationError(self.MSG_EDAD_INVALIDA)
        return data

    def clean_dni(self):
        data = self.cleaned_data['dni']
        if not (len(data) == 8 and data.isdigit()):
            raise ValidationError(self.MSG_DNI_INVALIDO)
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
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
        }


class CustomUserChangeForm(UserChangeForm, CustomUserForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'foto', 'fecha_nacimiento', 'dni')
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
        }


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('numero', 'nombre_completo', 'fecha_vencimiento', 'cvc', 'banco')
        widgets = { 
            'fecha_vencimiento': forms.TextInput(attrs={'placeholder': 'mm/yyyy'}),
        }


    MSG_FECHA_INVALIDA = 'Ingrese una fecha de vencimiento válida porfavor'
    MSG_NUMERO_INVALIDO = 'El numero de la tarjeta debe ser de 16 digitos exactamente'
    MSG_CVC_INVALIDO = 'El numero CVC debe ser de más de 3 caracteres'

    def clean_numero(self):
       data = self.cleaned_data['numero']
       num_sin_espacios = data.replace(' ', '')
       if len(num_sin_espacios) != 16:   # Digitos de tarjeta promedio. No aceptamos cosas raras
           raise ValidationError(self.MSG_NUMERO_INVALIDO)
       return data

    def clean_fecha_vencimiento(self):
        data = self.cleaned_data['fecha_vencimiento']
        fecha = data.split('/')

        today = date.today()
        mes = fecha[0]
        try:
            año = fecha[1]
        except IndexError:
            raise ValidationError(self.MSG_FECHA_INVALIDA)
        else:
            año_invalido = len(año.strip()) < 4
            mes_invalido = int(mes) > 12
            fecha_invalida = int(año) <= today.year and int(mes) < today.month
            if año_invalido or mes_invalido or fecha_invalida:
                raise ValidationError(self.MSG_FECHA_INVALIDA)
        return data

    def clean_cvc(self):
        data = self.cleaned_data['cvc']
        if len(data) < 3:
            raise ValidationError(self.MSG_CVC_INVALIDO)
        return data
