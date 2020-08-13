from django import forms

from .models import Radiasi

class RadiasiForm(forms.ModelForm):
    class Meta:
        model = Radiasi
        fields = [
            'tanggal',
            'radiasi',
        ]

        labels = {
            'tanggal': 'Tanggal',
            'radiasi': 'Radiasi '
        }

        widgets = {
            'tanggal': forms.TextInput(
                attrs= {
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#radiasidate',
                    'data-inputmask-alias': 'datetime',
                    'data-inputmask-inputformat': 'dd-MM-yyyy',
                    'data-mask': '',
                }
            ),
            'radiasi': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                }
            ),
        }