# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from datetime import date
from .models import CustomUser, Tarjeta, Public


class CustomUserForm:
    URL_FOTO_ANONIMA = 'http://sport-werkt.nl/wp-content/uploads/2018/12/profile.png'
    MSG_EDAD_INVALIDA = 'Fecha de nacimiento invalida'
    MSG_DNI_INVALIDO = 'El DNI debe tener 8 digitos sin separadores. Ej: 11222333'

    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']
        today = date.today()
        diferencia_de_años = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if diferencia_de_años < 18 or diferencia_de_años > 125:
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
    foto = forms.URLField(required=False)
    fecha_nacimiento = forms.DateField(
        help_text='Debe ser mayor de 18 años para poder reservar!',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    dni = forms.CharField()

    def save(self, commit=True):
        user = super().save()
        public_user = Public.objects.create(user=user)
        public_user.foto = self.cleaned_data.get('foto')
        public_user.fecha_nacimiento = self.cleaned_data.get(
            'fecha_nacimiento')
        public_user.dni = self.cleaned_data.get('dni')
        return user

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['password']

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class PublicUserChangeForm(UserChangeForm, CustomUserForm):

    def __init__(self, *args, **kargs):
        super(PublicUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['password']

    class Meta(UserChangeForm.Meta):
        model = Public
        fields = ('foto', 'fecha_nacimiento', 'dni')
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'type': 'date'}),
        }


class TarjetaForm(forms.ModelForm):
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
            if año_invalido or mes_invalido:
                raise ValidationError(self.MSG_FECHA_INVALIDA)
            elif date(int(año), int(mes), 1) <= date.today():
                raise ValidationError(self.MSG_FECHA_INVALIDA)
        return data

    def clean_cvc(self):
        data = self.cleaned_data['cvc']
        if len(data) < 3:
            raise ValidationError(self.MSG_CVC_INVALIDO)
        return data

    class Meta:
        model = Tarjeta
        fields = ('numero', 'nombre_completo',
                  'fecha_vencimiento', 'cvc', 'banco')
        widgets = {
            'fecha_vencimiento': forms.TextInput(attrs={'placeholder': 'mm/yyyy'}),
        }


class AdminCreationForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)
