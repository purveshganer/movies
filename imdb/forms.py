from django import forms
from imdb.models import TitleBasics

class TitleBasicsForm(forms.ModelForm):
    class meta:
        model = TitleBasics
        fields = '__all__'