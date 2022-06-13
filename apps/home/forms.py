from dataclasses import field
from django import forms
from .models import TBA


# creating a form
class FormTBA(forms.ModelForm):
    words = forms.CharField()

    class Meta:
        model = TBA
        fields = ['words']