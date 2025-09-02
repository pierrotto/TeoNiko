# forms.py
from django import forms
from .models import Category, Jewel


class JewelBaseFrom(forms.ModelForm):
    class Meta:
        model = Jewel
        fields = '__all__'


class JewelAddForm(JewelBaseFrom):
    pass

