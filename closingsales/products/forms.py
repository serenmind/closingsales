from django import forms
from .models import AdImage


class AdImageForm(forms.ModelForm):

    class Meta:
        model = AdImage
        fields = ('file', )
