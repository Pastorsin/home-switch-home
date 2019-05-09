from django import forms
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

    def clean(self):
        cleaned_data = super(ResidenciaForm, self).clean()
        print(cleaned_data)
        print('hola!')
