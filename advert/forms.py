from django import forms
from tinymce.widgets import TinyMCE

from .models import *


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title', 'body', 'category']
        widgets = {'body': TinyMCE(attrs={'cols': 80, 'rows': 30})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']
        widgets = {'body': TinyMCE(attrs={'cols': 80, 'rows': 30})}
