from django import forms
from .models import Pizza

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'text', 'price', 'cover']