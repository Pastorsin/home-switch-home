from django import forms
from datetime import date
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
        widget=forms.TextInput({'type': 'date'})
    )
    fecha_hasta = forms.DateField(
        label='Hasta',
        required=True,
        widget=forms.TextInput({'type': 'date'})
    )
