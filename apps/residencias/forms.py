import calendar
from django import forms
from datetime import timedelta, datetime, date
from django.core.exceptions import ValidationError
from .models import Residencia, Ubicacion


class UbicacionForm(forms.ModelForm):

    class Meta:
        model = Ubicacion
        fields = ('pais', 'provincia', 'ciudad', 'calle', 'numero')

    def __init__(self, *args, **kwargs):
        super(UbicacionForm, self).__init__(*args, **kwargs)
        for field in self.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs['class'] = 'form-control'


class ResidenciaForm(forms.ModelForm):
    precio_base = forms.FloatField(widget=forms.TextInput(
        attrs={'min': 1, 'type': 'number', 'step': '0.1'}),
        label='Precio'
    )

    class Meta:
        model = Residencia
        fields = ('nombre', 'foto', 'precio_base', 'descripcion')

    def __init__(self, *args, **kwargs):
        super(ResidenciaForm, self).__init__(*args, **kwargs)
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = 'form-control'


class BusquedaResidenciaForm(forms.Form):
    pais = forms.CharField(
        max_length=255,
        required=False
    )
    provincia = forms.CharField(
        max_length=255,
        required=False
    )
    ciudad = forms.CharField(
        max_length=255,
        required=False
    )
    fecha_inicio = forms.DateField(
        label='Desde',
        required=True,
        widget=forms.TextInput({'type': 'date'}),
        help_text='El rango de fechas no debe superar los 2 meses'
    )
    fecha_hasta = forms.DateField(
        label='Hasta',
        required=True,
        widget=forms.TextInput({'type': 'date'})
    )

    MSG_LONGITUD_INVALIDA = 'Búsqueda no realizada, el rango \
            de fechas no debe superar los 2 meses'

    MSG_RANGO_INVALIDO = 'Búsqueda no realizada, ingrese un \
            rango válido porfavor'

    def clean(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        if self.longitud_invalida(fecha_inicio, fecha_hasta):
            raise ValidationError(self.MSG_LONGITUD_INVALIDA)
        elif self.rango_invalido(fecha_inicio, fecha_hasta):
            raise ValidationError(self.MSG_RANGO_INVALIDO)

    def longitud_invalida(self, fecha_inicio, fecha_hasta):
        return fecha_inicio + timedelta(days=61) < fecha_hasta

    def rango_invalido(self, fecha_inicio, fecha_hasta):
        return fecha_inicio > fecha_hasta
