from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Queja, Tramite


class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['asunto', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(QuejaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('asunto', css_class='form-group col-md-6'),
                Column('municipio', css_class='form-group col-md-6'),
            ),


        )

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = ['respuesta', 'adjunto', 'conclusion_queja', 'nivel_solucion']