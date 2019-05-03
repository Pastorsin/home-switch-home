from django import forms

from .models import Residencia


class ResidenciaForm(forms.ModelForm):

    class Meta:
        model = Residencia
        exclude = ['fecha_publicacion']

    def __init__(self, *args, **kwargs):
        super(ResidenciaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
