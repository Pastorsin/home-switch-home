from django import forms
import datetime
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
    semana_ocupacion = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'min': 1, 'max': '52', 'type': 'number'}),
        help_text='La semana debe estar entre 1 y 52',
        label="Semana de ocupación del año {anio_siguiente}".format(
            anio_siguiente=datetime.date.today().year + 1)
    )
    precio_base = forms.FloatField(widget=forms.TextInput(
        attrs={'min': 1, 'type': 'number', 'step': '0.1'}),
        label='Precio'
    )

    class Meta:
        model = Residencia
        exclude = ['fecha_publicacion', 'ubicacion',
                   'estado', 'content_type', 'object_id']

    def __init__(self, *args, **kwargs):
        super(ResidenciaForm, self).__init__(*args, **kwargs)
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = 'form-control'
